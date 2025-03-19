import os
import time
import yaml
import subprocess
import numpy as np
import torch
from PIL import Image, ImageSequence, ImageOps
from check import check
from zhipuai import ZhipuAI


class cogview_3_flash_Node:
    def __init__(self):
        self.img_path = None
        self.img_data = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING",),
                "size": (["1024x1024", "768x1344", "864x1152", "1344x768", "1152x864", "1440x720", "720x1440"], {"default": "864x1152"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "IMAGE")
    RETURN_NAMES = ("bool", "image")
    FUNCTION = "cogview_3_flash"
    CATEGORY = "dong_tools/cogview_3_flash_by_dong"

    def cogview_3_flash(self, prompt, size, is_enable):
        # 获取 API 配置路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        api_path = os.path.join(os.path.dirname(os.path.dirname(script_dir)), "api_by_dong.yaml")

        if not is_enable:
            print("功能已禁用")
            return False, None

        if not check():
            print("未授权用户")
            return False, None

        if not os.path.exists(api_path):
            print("API key 文件未找到")
            return False, None
            
        with open(api_path, 'r') as file:
            api_keys = yaml.safe_load(file)
        api_key = api_keys.get('zhipuqingyan', {}).get('api_key')
        
        if not api_key:
            print("API key 未设置")
            return False, None



        # 调用 API 生成图像
        client = ZhipuAI(api_key=api_key)
        response = client.images.generations(
            model="cogview-3-flash",
            prompt=prompt,
            size=size,
        )

        if not response or not response.data:
            print("API 返回无效数据")
            return False, None

        url = response.data[0].url
        return True, self.download_image_from_url(url, None, is_enable)

    def download_image_from_url(self, url, file_name, is_enable):
        if not url or "http" not in url:
            print("无效的 URL")
            return None

        try:
            # 设置下载目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            img_temp_dir = os.path.join(current_dir, 'img_temp')
            os.makedirs(img_temp_dir, exist_ok=True)

            # 生成文件名
            timestamp = int(time.time())
            img_path = os.path.join(img_temp_dir, f"{file_name or 'image'}-{timestamp}.png")

            # 使用 aria2c 下载
            cmd = ["aria2c", "-o", os.path.basename(img_path), "-x", "16", "-s", "16", url, "-d", img_temp_dir]
            subprocess.run(cmd, check=True)

        except subprocess.CalledProcessError as e:
            print(f"下载图片失败: {str(e)}")
            return None

        # 处理图片
        try:
            img = Image.open(img_path)
            img_out = []

            for frame in ImageSequence.Iterator(img):
                frame = ImageOps.exif_transpose(frame)
                if frame.mode == "I":
                    frame = frame.point(lambda i: i * (1 / 256)).convert("L")
                image = frame.convert("RGB")
                image = np.array(image).astype(np.float32) / 255.0
                image = torch.from_numpy(image).unsqueeze(0)
                img_out.append(image)

            self.img_path = img_path
            self.img_data = img_out[0] if img_out else None

            return self.img_data

        except Exception as e:
            print(f"图片处理失败: {str(e)}")
            return None

    def download_image(self, url_or_path, file_name=None, is_enable=True):
        if not url_or_path:
            url_or_path = "https://imgapi.cn/api.php?zd=mobile&fl=meizi&gs=images&fl=mobile"

        time.sleep(1)

        if "http" in url_or_path:
            return self.download_image_from_url(url_or_path, file_name, is_enable)

        return None

    @classmethod
    def IS_CHANGED(cls, is_enable):
        return True
