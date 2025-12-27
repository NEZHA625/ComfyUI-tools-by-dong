import os
import json
import base64
import time
import yaml
import requests
from io import BytesIO
from torchvision import transforms
from check import check


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


# ---------------- 路径 ----------------

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")


class sora2:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"default": ""}),
            },
            "optional": {
                "aspect_ratio": (["portrait", "landscape"], {"default": "landscape"}),
                "duration": (["10", "15"], {"default": "10"}),
                "remove_watermark": ("BOOLEAN", {"default": True}),
                "model": (["sora-2-image-to-video"], {"default": "sora-2-image-to-video"}),
                "Channel": (["kie", "suchuang"], {"default": "kie"}),
                "seed": ("INT", {"default": 917724495}),
                "timeout": ("INT", {"default": 600}),
                "kie_api": ("STRING", {"default": ""}),
                "suchuang_api": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING", "BOOLEAN", "STRING")
    RETURN_NAMES = ("video_url", "state", "log")
    FUNCTION = "run"
    CATEGORY = "dong_tools/sora2_by_dong"

    # ---------------- 工具 ----------------

    def image_to_base64(self, img_tensor):
        img = img_tensor[0].permute(2, 0, 1)
        pil = transforms.ToPILImage()(img)
        buf = BytesIO()
        pil.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()

    def upload_image_kie(self, img_tensor, api_key):
        url = "https://kieai.redpandaai.co/api/file-base64-upload"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "base64Data": self.image_to_base64(img_tensor),
            "uploadPath": "images/base64",
            "fileName": f"sora2-{int(time.time() * 1000)}.png"
        }

        r = requests.post(url, headers=headers, json=payload, timeout=60)
        data = r.json()

        if not data.get("success"):
            return None

        return data["data"].get("downloadUrl")

    # ---------------- 主入口 ----------------

    def run(
        self,
        image,
        prompt,
        aspect_ratio="landscape",
        duration="10",
        remove_watermark=True,
        model="sora-2-image-to-video",
        Channel="kie",
        seed=917724495,
        timeout=600,
        kie_api="",
        suchuang_api="",
    ):

        log("========== sora2 节点启动 ==========")

        if not check():
            return ("", False, "未授权用户")

        # -------- API KEY 获取逻辑 --------

        kie_api_key_final = None
        if kie_api and kie_api.strip():
            kie_api_key_final = kie_api.strip()
            log("使用节点传入的 kie_api_key")
        else:
            if os.path.exists(api_path):
                with open(api_path, "r", encoding="utf-8") as f:
                    kie_api_key_final = (yaml.safe_load(f) or {}).get("kie", {}).get("api_key")
                if kie_api_key_final:
                    log("已从 api_by_dong.yaml 读取 kie_api")

        suchuang_api_key_final = None
        if suchuang_api and suchuang_api.strip():
            suchuang_api_key_final = suchuang_api.strip()
            log("使用节点传入的 suchuang_api_key")
        else:
            if os.path.exists(api_path):
                with open(api_path, "r", encoding="utf-8") as f:
                    suchuang_api_key_final = (yaml.safe_load(f) or {}).get("suchuang", {}).get("api_key")
                if suchuang_api_key_final:
                    log("已从 api_by_dong.yaml 读取 suchuang_api")

        channel = Channel

        if channel == "kie" and not kie_api_key_final:
            return ("", False, "kie API Key 为空")

        if channel == "suchuang":
            if not kie_api_key_final:
                return ("", False, "kie API Key 为空")
            if not suchuang_api_key_final:
                return ("", False, "suchuang API Key 为空")

        # -------- 轮询参数 --------

        poll_interval = 5
        max_retry = max(1, timeout // poll_interval)

        # -------- 上传图片（统一 KIE）--------

        log("开始上传图片到 KIE")
        image_url = self.upload_image_kie(image, kie_api_key_final)
        if image_url:
            print(image_url)
        if not image_url:
            return ("", False, "图片上传失败")

        # ================= KIE =================

        if channel == "kie":

            log("使用 KIE 通道生成")

            create_url = "https://api.kie.ai/api/v1/jobs/createTask"
            headers = {
                "Authorization": f"Bearer {kie_api_key_final}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": model,
                "input": {
                    "prompt": prompt,
                    "image_urls": [image_url],
                    "aspect_ratio": aspect_ratio,
                    "n_frames": duration,
                    "remove_watermark": remove_watermark,
                    "seed": seed,
                }
            }

            r = requests.post(create_url, headers=headers, json=payload, timeout=60)
            result = r.json()

            task_id = (result.get("data") or {}).get("taskId")
            if not task_id:
                return ("", False, json.dumps(result, ensure_ascii=False))

            query_url = "https://api.kie.ai/api/v1/jobs/recordInfo"

            for i in range(max_retry):
                log(f"KIE 轮询 {i+1}/{max_retry}")
                time.sleep(poll_interval)

                r = requests.get(query_url, headers=headers, params={"taskId": task_id}, timeout=30)
                data = r.json().get("data", {})
                state = data.get("state")

                if state == "success":
                    result_json = json.loads(data.get("resultJson", "{}"))
                    urls = result_json.get("resultUrls", [])
                    if urls:
                        return (urls[0], True, f"KIE 成功 | task_id={task_id}")
                    return ("", False, "KIE 成功但无视频地址")

                if state == "fail":
                    return ("", False, data.get("failMsg", "KIE 生成失败"))

            return ("", False, "KIE 任务超时")

        # ================= 速创 =================

        log("使用 suchuang 通道生成")

        submit_url = "https://api.wuyinkeji.com/api/sora2/submit"
        
        headers = {
            "Authorization": suchuang_api_key_final,
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        
        if aspect_ratio == "portrait":
            aspect_ratio_value = "9:16"
        elif aspect_ratio == "landscape":
            aspect_ratio_value = "16:9"
        else:
            aspect_ratio_value = aspect_ratio  # 兜底，防止传入其他值
        data = {
            "prompt": prompt,
            "url": image_url,
            "aspectRatio": aspect_ratio_value,
            "duration": duration,
        }


        r = requests.post(
            submit_url,
            headers=headers,
            params={"key": suchuang_api_key_final},
            data=data,
            timeout=60
        )
        submit_result = r.json()

        if submit_result.get("code") != 200:
            return ("", False, json.dumps(submit_result, ensure_ascii=False))

        task_id = submit_result.get("data", {}).get("id")
        if not task_id:
            return ("", False, "suchuang未返回 task_id")

        detail_url = "https://api.wuyinkeji.com/api/sora2/detail"

        for i in range(max_retry):
            log(f"速创轮询 {i+1}/{max_retry}")
            time.sleep(poll_interval)

            r = requests.get(
                detail_url,
                headers=headers,
                params={"key": suchuang_api_key_final, "id": task_id},
                timeout=30
            )
            detail = r.json()

            if detail.get("code") != 200:
                continue

            data = detail.get("data", {})
            status = data.get("status")

            if status in (0, 3):
                continue

            if status == 1:
                return (data.get("remote_url"), True, f"速创成功 | task_id={task_id}")

            if status == 2:
                return ("", False, data.get("fail_reason", "速创生成失败"))

        return ("", False, "速创任务超时")
