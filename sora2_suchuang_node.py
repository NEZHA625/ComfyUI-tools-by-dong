import os
import json
import base64
import time
import yaml
import requests
from io import BytesIO
from PIL import Image
from torchvision import transforms
from check import check


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


# ---------------- 路径 ----------------

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")


class sora2_suchuang_node:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"default": ""}),
            },
            "optional": {
                "aspect_ratio": (["9:16", "16:9"], {"default": "9:16"}),
                "duration": (["10", "15"], {"default": "10"}),
            }
        }

    RETURN_TYPES = ("STRING", "BOOLEAN", "STRING")
    RETURN_NAMES = ("video_url", "state", "log")
    FUNCTION = "run"
    CATEGORY = "dong_tools/sora2_by_dong"

    # ---------------- 图片工具（KIE） ----------------

    def image_to_base64(self, img_tensor):
        log("STEP 2-1 开始转换 IMAGE → Base64")
        img = img_tensor[0].permute(2, 0, 1)
        pil = transforms.ToPILImage()(img)
        buf = BytesIO()
        pil.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        log("STEP 2-1 Base64 转换完成")
        return b64

    def upload_image(self, img_tensor, kie_api_key):
        log("STEP 2-2 开始上传图片到 KIE")

        url = "https://kieai.redpandaai.co/api/file-base64-upload"
        headers = {
            "Authorization": f"Bearer {kie_api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "base64Data": self.image_to_base64(img_tensor),
            "uploadPath": "images/base64",
            "fileName": f"sora2-{int(time.time() * 1000)}.png"
        }

        try:
            r = requests.post(url, headers=headers, json=payload, timeout=60)
            data = r.json()
        except Exception as e:
            log(f"❌ 图片上传请求异常: {e}")
            return None

        if not data.get("success"):
            log(f"❌ 图片上传失败: {data}")
            return None

        image_url = data["data"].get("downloadUrl")
        log(f"✅ 图片上传成功: {image_url}")
        return image_url

    # ---------------- 主逻辑 ----------------

    def run(self, image, prompt, aspect_ratio="9:16", duration="10"):

        log("========== sora2 节点开始执行 ==========")

        # STEP 1 授权校验
        log("STEP 1 开始授权校验")
        if not check():
            log("❌ 授权失败")
            return ("", False, "未授权用户")
        log("✅ 授权通过")

        if not os.path.exists(api_path):
            log("❌ api_by_dong.yaml 不存在")
            return ("", False, "api_key 未设置")

        with open(api_path, "r", encoding="utf-8") as f:
            api_cfg = yaml.safe_load(f) or {}

        kie_api_key = api_cfg.get("kie", {}).get("api_key")
        suchuang_api_key = api_cfg.get("suchuang", {}).get("api_key")

        if not kie_api_key:
            log("❌ kie api_key 未配置")
            return ("", False, "kie api_key 未配置")

        if not suchuang_api_key:
            log("❌ suchuang api_key 未配置")
            return ("", False, "suchuang api_key 未配置")

        log("✅ API Key 加载完成")

        # STEP 2 上传图片
        image_url = self.upload_image(image, kie_api_key)
        if not image_url:
            return ("", False, "图片上传失败")

        # STEP 3 提交 sora2 任务
        log("STEP 3 提交 sora2 生成任务")

        submit_url = "https://api.wuyinkeji.com/api/sora2/submit"
        headers = {
            "Authorization": suchuang_api_key,
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
        }

        data = {
            "prompt": prompt,
            "url": image_url,
            "aspectRatio": aspect_ratio,
            "duration": duration,
        }

        try:
            r = requests.post(
                submit_url,
                headers=headers,
                params={"key": suchuang_api_key},
                data=data,
                timeout=60
            )
            submit_result = r.json()
            log(f"提交返回: {submit_result}")
        except Exception as e:
            log(f"❌ 提交任务异常: {e}")
            return ("", False, f"提交失败: {e}")

        if submit_result.get("code") != 200:
            log("❌ 提交失败")
            return ("", False, json.dumps(submit_result, ensure_ascii=False))

        task_id = submit_result.get("data", {}).get("id")
        if not task_id:
            log("❌ 未获取 task_id")
            return ("", False, "提交成功但未返回任务ID")

        log(f"✅ 任务提交成功，task_id={task_id}")

        # STEP 4 查询任务状态
        log("STEP 4 开始轮询任务状态")

        detail_url = "https://api.wuyinkeji.com/api/sora2/detail"

        for i in range(60):
            log(f"轮询第 {i + 1} 次")
            time.sleep(5)

            try:
                r = requests.get(
                    detail_url,
                    headers=headers,
                    params={"key": suchuang_api_key, "id": task_id},
                    timeout=30
                )
                detail_result = r.json()
            except Exception as e:
                log(f"查询异常: {e}")
                continue

            if detail_result.get("code") != 200:
                log(f"状态接口异常: {detail_result}")
                continue

            data = detail_result.get("data", {})
            status = data.get("status")
            log(f"当前状态 status={status}")

            if status in (0, 3):
                continue

            if status == 1:
                video_url = data.get("remote_url")
                log(f"✅ 生成成功: {video_url}")
                return (video_url, True, f"生成成功 | task_id={task_id}")

            if status == 2:
                reason = data.get("fail_reason", "生成失败")
                log(f"❌ 生成失败: {reason}")
                return ("", False, reason)

        log("❌ 任务超时未完成")
        return ("", False, "任务超时未完成")
