import json
import os
import time
from check import check
import shutil
import requests
from huggingface_hub import HfApi
from urllib3.util.retry import Retry
import yaml
from requests.adapters import HTTPAdapter
from torchvision import transforms
import torch
import re
from PIL import Image, PngImagePlugin
import base64
from io import BytesIO

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")

class GLM_Node:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "image": ("IMAGE",),
            },
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "Please provide a detailed description of this image. If any characters in the image are familiar to you, such as celebrities, movie characters, or animated figures, please directly use their names. The description should be as detailed as possible, but should not exceed 200 words."}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "GLM"
    CATEGORY = "dong_tools/img_understanding_by_v2_by_dong"

    def GLM(self, image=None, prompt=""):
        def image2base64(image):
            image_single = image[0]
            image_single = image_single.permute(2, 0, 1)
            to_pil = transforms.ToPILImage()
            img = to_pil(image_single)
            buffered = BytesIO()
            img.save(buffered, format="png")
            return base64.b64encode(buffered.getvalue()).decode("utf-8")

        if not check():
            return ("未授权用户",)

        if not os.path.exists(api_path):
            return ("api_key未设置，请使用set_api节点设置api",)

        with open(api_path, "r") as file:
            api_keys = yaml.safe_load(file)
        api_key = api_keys["siliconflow"]["api_key"]

        base64_image = None
        if image is not None:
            base64_image = image2base64(image)

        def request_with_retry(func, retries=3, delay=5):
            for i in range(retries):
                try:
                    return func()
                except Exception as e:
                    print(f"请求异常: {e}，第{i+1}次重试...")
                    time.sleep(delay)
            return None

        def siliconflow():
            def call():
                url = "https://api.siliconflow.cn/v1/chat/completions"
                model = "THUDM/GLM-4.1V-9B-Thinking"
        
                content = []
                if base64_image:
                    content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}",
                            "detail": "high"
                        }
                    })
                content.append({"type": "text", "text": prompt})
        
                payload = {
                    "model": model,
                    "messages": [{"role": "user", "content": content}],
                    "stream": True,   # ✅ 流式输出
                    "max_tokens": 8192,
                    "stop": ["null"],
                    "temperature": 0.7,
                    "top_p": 0.7,
                    "top_k": 50,
                    "frequency_penalty": 0.5,
                    "n": 1,
                    "response_format": {"type": "text"},
                }
                headers = {
                    "Authorization": "Bearer " + api_key,
                    "Content-Type": "application/json"
                }
        
                final_content = []
                print("\n\nThink:")
                with requests.post(url, json=payload, headers=headers, stream=True, timeout=60) as r:
                    r.raise_for_status()
                    for line in r.iter_lines():
                        if not line:
                            continue
                        if line.startswith(b"data: "):
                            data = line[len(b"data: "):].decode("utf-8")
                            if data.strip() == "[DONE]":
                                break
                            try:
                                obj = json.loads(data)
                                delta = obj["choices"][0]["delta"]
                                
                                # ✅ 流式打印 reasoning_content
                                if "reasoning_content" in delta and delta["reasoning_content"]:
                                    print(delta["reasoning_content"], end="", flush=True)
        
                                # ✅ 收集最终回答，过滤掉 None
                                if "content" in delta and delta["content"]:
                                    final_content.append(delta["content"])
        
                            except Exception as e:
                                print(f"解析流式数据出错: {e}")
        
                print("\n")  # 输出结束换行
                return "".join(final_content) if final_content else "无内容返回"
        
            return request_with_retry(call)

        result = siliconflow()
        if result is None:
            return ("SiliconFlow 请求失败或超时",)
        return (result,)

    @classmethod
    def IS_CHANGED(s):
        return True
