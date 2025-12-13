import requests
import json
import yaml
import os
from check import check

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")


class kie_nano_post_node:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_url1": ("STRING", {"default": ""}),
                "image_url2": ("STRING", {"default": ""}),
                "image_url3": ("STRING", {"default": ""}),
                "image_url4": ("STRING", {"default": ""}),
                "image_url5": ("STRING", {"default": ""}),
                "image_url6": ("STRING", {"default": ""}),
                "image_url7": ("STRING", {"default": ""}),
                "image_url8": ("STRING", {"default": ""}),
                "model": (["nano-banana-pro"], {"default": "nano-banana-pro"}),
                "prompt": ("STRING", {"default": ""}),
                "aspect_ratio": (["1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9","auto"], {"default": "auto"}),
                "resolution": (["1K","2K","4K"], {"default": "2K"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("task_id",)
    FUNCTION = "send_request"
    CATEGORY = "dong_tools/nano_by_dong"

    def send_request(self, image_url1, image_url2, image_url3, image_url4,
                     image_url5, image_url6, image_url7, image_url8,
                     model, prompt, aspect_ratio, resolution):

        # --- 权限检查 ---
        if not check():
            return ("未授权用户",)

        # --- API KEY 检查 ---
        if not os.path.exists(api_path):
            return ("api_key未设置，请使用set_api节点设置api",)

        with open(api_path, "r") as file:
            api_keys = yaml.safe_load(file)
        api_key = api_keys["kie"]["api_key"]

        # --- 请求地址与 headers ---
        url = "https://api.kie.ai/api/v1/jobs/createTask"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # --- 准备 payload ---
        payload = {
            "model": model,
            "callBackUrl": "https://your-domain.com/api/callback",
            "input": {
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "resolution": resolution,
                "output_format": "png",
            }
        }

        # --- 组装 image_input（自动过滤空值） ---
        image_inputs = [
            u for u in [
                image_url1, image_url2, image_url3, image_url4,
                image_url5, image_url6, image_url7, image_url8
            ] if u and u.strip() != ""
        ]

        if image_inputs:
            payload["input"]["image_input"] = image_inputs

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            result = response.json()

            # --- 避免 NoneType 崩溃 ---
            data = result.get("data") or {}

            task_id = data.get("taskId")

            # 如果 task_id 不存在，返回完整错误信息
            if not task_id:
                return (json.dumps(result, ensure_ascii=False),)

            return (task_id,)

        except Exception as e:
            return (f"Error: {str(e)}",)
