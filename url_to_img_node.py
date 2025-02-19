import locale
import os
import time
import requests
import subprocess
from PIL import Image, ImageOps, ImageSequence
import numpy as np
import torch
import configparser
import random
from check import check
class ImageDownloader:  
    def __init__(self):
        self.img_path = None
        self.img_data = None
        self._current_index = 0  # 初始化 _current_index

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "url_or_path": ("STRING", {"default": "https://imgapi.cn/api.php?zd=mobile&fl=meizi&gs=images&fl=mobile"}),
                "file_name": ("STRING", {}),
                "iterator_mode": (["sequential", "random", "Infinite"], {"default": "sequential"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("img", "log")

    FUNCTION = "download_image"  # 函数入口
    CATEGORY = "dong_tools/download_img_by_dong"

    def download_image_from_url(self, url_or_path, file_name, is_enable):
        url = url_or_path
        if not check():
            print("未授权用户")
            return (False,)
        if not is_enable:
            return (self.img_data, "功能已禁用")
        if url is None or "http" not in url:
            return (None, "无效的URL")

        # 使用 aria2c 进行多线程下载
        try:
            # 构建 img_temp 目录路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            img_temp_dir = os.path.join(current_dir, 'img_temp')
            os.makedirs(img_temp_dir, exist_ok=True)

            # 时间戳
            timestamp = int(time.time())
            if file_name is None:
                img_path = os.path.join(img_temp_dir, f'image-{timestamp}.png')
            else:
                img_path = os.path.join(img_temp_dir, f'{file_name}-{timestamp}.png')

            cmd = [
                "aria2c", "-o", os.path.basename(img_path), "-x", "16", "-s", "16", url, "-d", img_temp_dir
            ]
            subprocess.run(cmd, check=True)

        except subprocess.CalledProcessError as e:
            return (None, f"下载图片失败: {str(e)}")

        # 检查图片格式并打开
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
            img_out = img_out[0]
            self.img_path = img_path
            self.img_data = img_out

            return (img_out, f"图片文件已保存: {img_path}")

        except Exception as e:
            return (None, f"图片处理失败: {str(e)}")

    def download_image_from_path(self, url_or_path, file_name, is_enable, iterator_mode):
        path = url_or_path
        if not is_enable:
            return (self.img_data, "功能已禁用")

        if not os.path.exists(path):
            return (None, "文件夹不存在")

        try:
            image_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            if not image_files:
                return (None, "文件夹中无图片")

            # 根据 iterator_mode 选择图片
            if iterator_mode == "random":
                selected_file = random.choice(image_files)
            elif iterator_mode == "Infinite":
                # 无限模式：循环遍历所有文件
                if not hasattr(self, '_current_index'):
                    self._current_index = 0
                selected_file = image_files[self._current_index % len(image_files)]
                self._current_index += 1
            else:  # 默认使用顺序模式
                if not hasattr(self, '_current_index'):
                    self._current_index = 0
                selected_file = image_files[self._current_index]
                self._current_index = (self._current_index + 1) % len(image_files)

            img_path = os.path.join(path, selected_file)

            # 检查图片格式并打开
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
            img_out = img_out[0]

            self.img_path = img_path
            self.img_data = img_out

            return (img_out, f"图片文件已保存: {img_path}")

        except Exception as e:
            return (None, f"图片处理失败: {str(e)}")



    def download_image(self, url_or_path, file_name=None, is_enable=True, iterator_mode="sequential"):
        if url_or_path == "":
            url_or_path = "https://imgapi.cn/api.php?zd=mobile&fl=meizi&gs=images&fl=mobile"
        time.sleep(1)
        if "http" in url_or_path:
            return self.download_image_from_url(url_or_path, file_name, is_enable)
        else:
            return self.download_image_from_path(url_or_path, file_name, is_enable, iterator_mode)

    @classmethod
    def IS_CHANGED(cls, is_enable):
        return True
