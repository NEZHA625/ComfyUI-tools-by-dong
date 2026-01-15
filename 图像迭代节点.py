import os
import random
import torch
import numpy as np
from PIL import Image, ImageOps, ImageSequence
import re
import locale
import sys
import ctypes
import functools

def pillow(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"Pillow Error: {e}")
        return None

if sys.platform.startswith("win"):
    _strcmp = ctypes.windll.Shlwapi.StrCmpLogicalW

    def windows_strcmp(a, b):
        return _strcmp(str(a), str(b))

    windows_sort_key = functools.cmp_to_key(windows_strcmp)

def get_locale():
    """根据平台选择合适的 locale"""
    try:
        if sys.platform.startswith("win"):
            locale.setlocale(locale.LC_ALL, "")
        else:
            try:
                locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")
            except locale.Error:
                locale.setlocale(locale.LC_ALL, "C")
    except Exception:
        locale.setlocale(locale.LC_ALL, "C")

get_locale()

def natural_sort_key(s):
    """自然排序：数字按数值，字母忽略大小写，中文按拼音/locale"""
    parts = re.split(r'(\d+)', os.path.basename(s))
    key = []
    for part in parts:
        if part.isdigit():
            key.append(int(part))
        else:
            key.append(locale.strxfrm(part.lower()))
    return key

class 图像迭代节点:
    def __init__(self):
        self.index = 0
        self.record = 0
        self.path = None
        self.image_files = []

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "图片文件夹": ("STRING", {"default": ""}),
                "节点开关": ("BOOLEAN", {"default": True}),
                "动态刷新": ("BOOLEAN", {"default": False}),
                "递归子文件夹": ("BOOLEAN", {"default": False}),  
                "迭代模式": (
                    ["顺序", "随机", "无限", "顺序结束"], 
                    {"default": "顺序"}
                ),
                "排序模式": (
                    ["名称", "时间"],  
                    {"default": "名称"}
                ),
            }
        }

    RETURN_TYPES = ("IMAGE", "BOOLEAN")
    RETURN_NAMES = ("image", "is_end")
    FUNCTION = "file"
    CATEGORY = "dong_tools/image_iterator_by_dong"

    def load_images(self, 图片文件夹, 递归子文件夹=True, 排序模式="名称"):
        """收集文件夹下的所有图片，可选择递归子文件夹，并支持排序方式"""
        image_files = []
        if 递归子文件夹:
            for root, _, files in os.walk(图片文件夹):
                for f in files:
                    if f.lower().endswith((
                        ".png", ".jpg", ".jpeg", ".gif", ".bmp", 
                        ".tiff", ".tif", ".webp", ".svg", ".ico", ".raw"
                    )):
                        image_files.append(os.path.join(root, f))
        else:
            for f in os.listdir(图片文件夹):
                file_path = os.path.join(图片文件夹, f)
                if os.path.isfile(file_path) and f.lower().endswith((
                    ".png", ".jpg", ".jpeg", ".gif", ".bmp", 
                    ".tiff", ".tif", ".webp", ".svg", ".ico", ".raw"
                )):
                    image_files.append(file_path)

        # 排序方式选择
        if 排序模式 == "时间":
            image_files = sorted(image_files, key=lambda x: os.path.getmtime(x))
        else:  # 默认按名称
            if sys.platform.startswith("win"):
                image_files = sorted(image_files, key=windows_sort_key)
            else:
                image_files = sorted(image_files, key=natural_sort_key)

        return image_files

    def file(
        self, 图片文件夹, 迭代模式="顺序", 排序模式="名称", 节点开关=True, 动态刷新=False, 递归子文件夹=True
    ):
        flag_is_end = False
        if not 节点开关:
            return (None, flag_is_end)

        # 如果路径改变或者强制刷新，重新加载文件列表
        if self.path != 图片文件夹 or 动态刷新:
            self.index = 0
            self.path = 图片文件夹
            self.image_files = self.load_images(图片文件夹, 递归子文件夹, 排序模式)

        if not self.image_files:
            return (None, flag_is_end)

        # 越界处理
        if self.index >= len(self.image_files):
            self.index = 0
            if 迭代模式 == "顺序":
                return (None, True)

        if self.index == len(self.image_files) - 1 and 迭代模式 == "顺序结束":
            flag_is_end = True

        # 读取图像
        image_path = self.image_files[self.index]
        img = pillow(Image.open, image_path)
        if img is None:
            return (None, flag_is_end)

        output_images = []
        w, h = None, None
        excluded_formats = ["MPO"]

        for i in ImageSequence.Iterator(img):
            i = pillow(ImageOps.exif_transpose, i)
            if i.mode == "I":
                i = i.point(lambda i: i * (1 / 255))
            image = i.convert("RGB")

            if len(output_images) == 0:
                w, h = image.size

            if image.size != (w, h):
                continue

            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]

            if "A" in i.getbands():
                mask = np.array(i.getchannel("A")).astype(np.float32) / 255.0
                mask = 1.0 - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

            output_images.append(image)

        if len(output_images) > 1 and img.format not in excluded_formats:
            output_image = torch.cat(output_images, dim=0)
        else:
            output_image = output_images[0]

        if 迭代模式 in ["顺序", "无限", "顺序结束"]:
            self.index += 1
        elif 迭代模式 == "随机":
            self.index = random.randint(0, len(self.image_files) - 1)

        return (output_image, flag_is_end)

    @classmethod
    def IS_CHANGED(self, s):
        self.record = self.index
        return self.record
