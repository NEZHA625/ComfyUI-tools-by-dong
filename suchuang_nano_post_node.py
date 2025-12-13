import requests
import json
import yaml
import os
from check import check

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")


class suchuang_nano_post_node:
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
                "resolution": (["1K","2K","4K"], {"default": "1K"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("task_id",)
    FUNCTION = "send_request"
    CATEGORY = "dong_tools/suchuang_nano_post_by_dong"

    def send_request(self, 
                     image_url1, image_url2, image_url3, image_url4,
                     image_url5, image_url6, image_url7, image_url8,model,prompt,
                     aspect_ratio, resolution):

        # --- 权限检查 ---
        if not check():
            return ("未授权用户",)

        # --- API KEY 检查 ---
        if not os.path.exists(api_path):
            return ("api_key未设置，请使用 set_api 节点设置 api",)

        with open(api_path, "r") as file:
            api_keys = yaml.safe_load(file)
        api_key = api_keys["suchuang"]["api_key"]

        # --- 五音科技 真实 POST 地址 ---
        url = "https://api.wuyinkeji.com/api/img/nanoBanana-pro"

        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": api_key,
        }

        # --- 组装 img_url 数组（自动过滤空） ---
        img_urls = [
            u for u in [
                image_url1, image_url2, image_url3, image_url4,
                image_url5, image_url6, image_url7, image_url8
            ] if u and u.strip() != ""
        ]

        # --- 构建 payload ---
        payload = {
            "prompt": prompt,
            "aspectRatio": aspect_ratio,
            "imageSize": resolution,
        }

        if img_urls:
            payload["img_url"] = img_urls
        else:
            payload["img_url"] = []

        try:
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()

            # data.id 为任务 ID
            data = result.get("data") or {}
            task_id = data.get("id")

            if not task_id:
                return (json.dumps(result, ensure_ascii=False),)

            return (str(task_id),)

        except Exception as e:
            return (f"Error: {str(e)}",)
