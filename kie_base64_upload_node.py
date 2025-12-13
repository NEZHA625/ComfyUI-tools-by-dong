import os
import json
import base64
import requests
import yaml
import time
from io import BytesIO
from PIL import Image
from torchvision import transforms
from check import check

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")


class kie_base64_upload_node:
    def __init__(self):
        pass

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
            }
        }

    RETURN_TYPES = (
        "STRING","STRING","STRING","STRING",
        "STRING","STRING","STRING","STRING"
    )

    RETURN_NAMES = (
        "image1_url","image2_url","image3_url","image4_url",
        "image5_url","image6_url","image7_url","image8_url"
    )

    FUNCTION = "upload_images"
    CATEGORY = "dong_tools/upload_by_dong"

    def upload_images(self, **images):

        # -------- 授权检查 --------
        if not check():
            return ("未授权用户",) * 8

        if not os.path.exists(api_path):
            return ("api_key未设置，请使用set_api节点设置api",) * 8

        with open(api_path, "r") as f:
            api_keys = yaml.safe_load(f)
        api_key = api_keys["kie"]["api_key"]

        # -------- 转 Base64 --------
        def image_to_base64(img_tensor):
            img_single = img_tensor[0]
            img_single = img_single.permute(2, 0, 1)
            pil_img = transforms.ToPILImage()(img_single)
            buf = BytesIO()
            pil_img.save(buf, format="PNG")
            return base64.b64encode(buf.getvalue()).decode("utf-8")

        # -------- 上传函数 --------
        def upload_single(img_tensor):
            if img_tensor is None:
                return ""

            base64_data = image_to_base64(img_tensor)
            file_name = f"uploaded-{int(time.time() * 1000)}.png"

            url = "https://kieai.redpandaai.co/api/file-base64-upload"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "base64Data": base64_data,
                "uploadPath": "images/base64",
                "fileName": file_name
            }

            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                result = response.json()

                if not result.get("success"):
                    return ""

                return result["data"].get("downloadUrl", "")

            except Exception:
                return ""

        # -------- 遍历 8 张图 --------
        output_urls = []
        for i in range(1, 9):
            key = f"image{i}"
            output_urls.append(upload_single(images.get(key)))

        return tuple(output_urls)
