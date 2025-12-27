import os
import json
import base64
import time
import yaml
import requests
import sys
from io import BytesIO
from PIL import Image
import numpy as np
import torch
from torchvision import transforms
from check import check


ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")


class nano_banana_node:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "image3": ("IMAGE",),
                "image4": ("IMAGE",),
                "image5": ("IMAGE",),
                "image6": ("IMAGE",),
                "image7": ("IMAGE",),
                "image8": ("IMAGE",),
                "model": (["nano-banana-pro","nano-banana"],{"default": "nano-banana-pro"}),
                "prompt": ("STRING", {"default": ""}),
                "aspect_ratio": ([
                    "1:1","2:3","3:2","3:4","4:3",
                    "4:5","5:4","9:16","16:9","21:9","auto"
                ], {"default": "auto"}),
                "resolution": (["1K","2K","4K"], {"default": "2K"}),
                "seed": ("INT", {"default": 917724495}),
                "channel": (["kie","suchuang"], {"default": "kie"}),
                "timeout": ("INT", {"default": 600}),
                "kie_api": ("STRING", {"default": ""}), 
                "suchuang_api": ("STRING", {"default": ""}), 
            }
        }

    RETURN_TYPES = ("IMAGE", "BOOLEAN", "STRING")
    RETURN_NAMES = ("image", "state", "log")
    FUNCTION = "run"
    CATEGORY = "dong_tools/nano_banana_by_dong"

    # ================= 工具函数 =================

    def image_to_base64(self, img_tensor):
        img = img_tensor[0].permute(2, 0, 1)
        pil = transforms.ToPILImage()(img)
        buf = BytesIO()
        pil.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")

    def upload_image(self, img_tensor, kie_api_key):
        url = "https://kieai.redpandaai.co/api/file-base64-upload"
        headers = {
            "Authorization": f"Bearer {kie_api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "base64Data": self.image_to_base64(img_tensor),
            "uploadPath": "images/base64",
            "fileName": f"upload-{int(time.time() * 1000)}.png"
        }

        try:
            r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
            data = r.json()
            if not data.get("success"):
                return None
            return data["data"].get("downloadUrl")
        except Exception:
            return None

    def download_image(self, url):
        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()
    
        total = int(r.headers.get("Content-Length", 0))
        downloaded = 0
        chunk_size = 8192
    
        buffer = BytesIO()
    
        for chunk in r.iter_content(chunk_size=chunk_size):
            if not chunk:
                continue
    
            buffer.write(chunk)
            downloaded += len(chunk)
    
            if total > 0:
                percent = downloaded / total * 100
                sys.stdout.write(
                    f"\r下载图片中: {percent:6.2f}% "
                    f"({downloaded / 1024:.1f} KB / {total / 1024:.1f} KB)"
                )
                sys.stdout.flush()
    
        print()  # 换行
    
        buffer.seek(0)
        img = Image.open(buffer).convert("RGB")
        arr = np.array(img).astype(np.float32) / 255.0
        tensor = torch.from_numpy(arr).unsqueeze(0)
    
        return tensor
        
    # def download_image(self, url):
    #     r = requests.get(url, timeout=60)
    #     img = Image.open(BytesIO(r.content)).convert("RGB")
    #     arr = np.array(img).astype(np.float32) / 255.0
    #     tensor = torch.from_numpy(arr).unsqueeze(0)
    #     return tensor

    # ================= 主逻辑 =================

    def run(
        self,
        model="nano-banana-pro",
        prompt="",
        aspect_ratio="auto",
        resolution="2K",
        seed=0,
        channel="kie",
        timeout=600,
        kie_api="",
        suchuang_api="",
        **images
    ):

        log_lines = []
        
        CYAN  = "\033[36m"
        GREEN = "\033[32m"
        RED   = "\033[31m"
        RESET = "\033[0m"
        
        def log(msg, level="info"):
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            text = f"[banana][{t}] {msg}"
            log_lines.append(text)
        
            if level == "success":
                color = GREEN
            elif level == "error":
                color = RED
            else:
                color = CYAN
        
            print(f"{color}{text}{RESET}")


        log("========== nano-banana 节点开始运行 ==========")

        # -------- 权限检查 --------
        log("执行授权检查")
        if not check():
            return (None, False, "未授权用户")
        log("授权检查通过")

        # -------- API KEY 获取逻辑 --------
        kie_api_key_final = None
        if kie_api and kie_api.strip():
            kie_api_key_final = kie_api.strip()
            log("使用节点传入的 kie_api_key")
        else:
            if os.path.exists(api_path):
                with open(api_path, "r", encoding="utf-8") as f:
                    kie_api_key_final = yaml.safe_load(f).get("kie", {}).get("api_key")
                if kie_api_key_final:
                    log("已从 api_by_dong.yaml 读取 kie_api")
        
        suchuang_api_key_final = None
        if suchuang_api and suchuang_api.strip():
            suchuang_api_key_final = suchuang_api.strip()
            log("使用节点传入的 suchuang_api_key")
        else:
            if os.path.exists(api_path):
                with open(api_path, "r", encoding="utf-8") as f:
                    suchuang_api_key_final = yaml.safe_load(f).get("suchuang", {}).get("api_key")
                if suchuang_api_key_final:
                    log("已从 api_by_dong.yaml 读取 suchuang_api")

        if channel == "kie" and not kie_api_key_final:
            return (None, False, "kie API Key 为空")
        if channel == "suchuang" and not suchuang_api_key_final:
            if not kie_api_key_final:
                return (None, False, "kie API Key 为空")
            return (None, False, "suchuang API Key 为空")

        # -------- 上传图片 --------
        image_urls = []
        for i in range(1, 9):
            img = images.get(f"image{i}")
            if img is not None:
                log(f"检测到 image{i}，开始上传")
                log("开始将 IMAGE Tensor 转为 Base64")
                b64_len = len(self.image_to_base64(img))
                log(f"Base64 转换完成，长度={b64_len}")
                if kie_api_key_final:
                    url = self.upload_image(img, kie_api_key_final)
                    if url:
                        log(f"图片上传成功，downloadUrl={url}")
                        image_urls.append(url)

        log(f"图片上传完成，共成功 {len(image_urls)} 张")

        # -------- 根据 channel 调用接口 --------
        if channel == "kie":
            # -------- 创建任务（KIE） --------
            create_url = "https://api.kie.ai/api/v1/jobs/createTask"
            headers = {"Authorization": f"Bearer {kie_api_key_final}", "Content-Type": "application/json"}
            
            if model == "nano-banana":
                payload_model = "google/nano-banana-edit"
                payload = {
                    "model": payload_model,
                    "input": {
                        "prompt": prompt,
                        "output_format": "png",
                        "image_size": aspect_ratio
                    }
                }
            else:
                payload = {
                    "model": model,
                    "input": {
                        "prompt": prompt,
                        "aspect_ratio": aspect_ratio,
                        "resolution": resolution,
                        "output_format": "png",
                    }
                }
                
            if image_urls:
                if model == "nano-banana":
                    payload["input"]["image_urls"] = image_urls
                else:
                    payload["input"]["image_input"] = image_urls

            log("创建任务 payload：")
            log(json.dumps(payload, ensure_ascii=False, indent=2))

            try:
                r = requests.post(create_url, headers=headers, data=json.dumps(payload), timeout=60)
                result = r.json()
            except Exception as e:
                return (None, False, f"创建任务失败: {str(e)}")

            task_id = (result.get("data") or {}).get("taskId")
            if not task_id:
                return (None, False, json.dumps(result, ensure_ascii=False))

            log(f"任务创建成功，task_id={task_id}")

            # -------- 轮询官方 recordInfo --------
            poll_interval = 5
            max_retry = max(1, timeout // poll_interval)
            query_url = "https://api.kie.ai/api/v1/jobs/recordInfo"

            for i in range(max_retry):
                log(f"轮询 {i+1}/{max_retry}")
                try:
                    r = requests.get(query_url, params={"taskId": task_id}, headers=headers, timeout=30)
                    data = r.json().get("data", {})
                except Exception as e:
                    log(f"轮询请求异常: {e}")
                    data = {}

                state = data.get("state")
                if state:
                    log(f"当前状态={state}")

                if state == "success":
                    try:
                        result_urls = json.loads(data.get("resultJson", "{}")).get("resultUrls", [])
                        if result_urls:
                            log(f"图片下载地址: {result_urls[0]}")
                            img = self.download_image(result_urls[0])
                            return (img, True, f"生成成功 | task_id={task_id} | 用时≈{poll_interval*(i+1)} 秒")
                    except Exception as e:
                        return (None, False, f"下载图片失败: {e}")

                if state == "fail":
                    fail_msg = data.get("failMsg", "生成失败")
                    return (None, False, fail_msg)

                time.sleep(poll_interval)

            return (None, False, f"超时退出：{timeout} 秒内未完成 | task_id={task_id}")

        elif channel == "suchuang":
            # -------- 创建任务（Suchuang API） --------
            model_to_url = {
                "nano-banana": "https://api.wuyinkeji.com/api/img/nanoBanana",
                "nano-banana-pro": "https://api.wuyinkeji.com/api/img/nanoBanana-pro"
            }
        
            if model in model_to_url:
                create_url = model_to_url[model]
            else:
                raise ValueError(f"未知的模型: {model}")
        
            headers = {
                "Authorization": suchuang_api_key_final,
                "Content-Type": "application/json;charset:utf-8"
            }
        
            payload = {
                "prompt": prompt,
                "aspectRatio": aspect_ratio,
                "imageSize": resolution,
            }
            
            if model == "nano-banana":
                # 去掉 imageSize
                payload.pop("imageSize", None)
                # 增加 model 字段
                payload["model"] = "nano-banana"
         


            if image_urls:
                payload["img_url"] = image_urls

            log("创建任务 payload（Suchuang API）：")
            log(json.dumps(payload, ensure_ascii=False, indent=2))

            try:
                r = requests.post(create_url, headers=headers, data=json.dumps(payload), timeout=60)
                result = r.json()
            except Exception as e:
                return (None, False, f"创建任务失败: {str(e)}")

            if result.get("code") != 200 or "data" not in result:
                return (None, False, f"任务创建失败: {json.dumps(result, ensure_ascii=False)}")

            task_id = result["data"].get("id")
            log(f"任务创建成功，task_id={task_id}")

            # -------- 轮询 Suchuang 生成结果 --------
            poll_interval = 5
            max_retry = max(1, timeout // poll_interval)
            query_url = "https://api.wuyinkeji.com/api/img/drawDetail"

            for i in range(max_retry):
                log(f"轮询 {i+1}/{max_retry}")
                try:
                    r = requests.get(
                        query_url,
                        params={"key": suchuang_api_key_final, "id": task_id},
                        headers={"Authorization": suchuang_api_key_final, "Content-Type": "application/json;charset:utf-8"},
                        timeout=30
                    )
                    data = r.json().get("data", {})
                except Exception as e:
                    log(f"轮询请求异常: {e}")
                    data = {}

                status = data.get("status")
                status_dict = {
                                0: "排队中",
                                1: "生成中",
                                2: "成功",
                                3: "失败"
                            }
                log(f"当前状态={status} ({status_dict.get(status, '未知状态')})")

                if status == 2:  # 成功
                    img_url = data.get("image_url")
                    log(f"图片下载地址: {img_url}")
                    if img_url:
                        try:
                            img = self.download_image(img_url)
                            return (img, True, f"生成成功 | task_id={task_id} | 用时≈{poll_interval*(i+1)} 秒")
                        except Exception as e:
                            return (None, False, f"下载图片失败: {e}")

                elif status == 3:  # 失败
                    fail_msg = data.get("fail_reason", "生成失败")
                    return (None, False, fail_msg)

                time.sleep(poll_interval)

            return (None, False, f"超时退出：{timeout} 秒内未完成 | task_id={task_id}")
