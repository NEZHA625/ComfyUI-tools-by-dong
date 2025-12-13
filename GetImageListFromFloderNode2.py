import os
from PIL import Image
import torch
import numpy as np
from check import check
import sys
import ctypes
import functools

class GetImageListFromFloderNode2:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder": ("STRING",),  
                "is_enable": ("BOOLEAN", {"default": True}),
                "is_recursive": ("BOOLEAN", {"default": False}),  
            }
        }

    RETURN_TYPES = ("BOOLEAN", "IMAGE", "STRING")  
    RETURN_NAMES = ("bool", "images", "image_names") 
    FUNCTION = "process_images" 
    CATEGORY = "dong_tools/get_image_list_from_floder2_by_dong" 

    def process_images(self, folder, is_enable, is_recursive):
        if not is_enable:
            print("功能已禁用")
            return (False, None, None)

        if not check():
            print("未授权用户")
            return (False, None, None)

        valid_extensions = {'.png', '.jpg', '.jpeg', '.webp'}
        image_paths = []

        # 扫描文件夹
        if is_recursive:
            for root, _, files in os.walk(folder):
                for file in files:
                    if os.path.splitext(file)[1].lower() in valid_extensions:
                        image_paths.append(os.path.join(root, file))
        else:
            for f in os.listdir(folder):
                full_path = os.path.join(folder, f)
                if os.path.isfile(full_path) and os.path.splitext(f)[1].lower() in valid_extensions:
                    image_paths.append(full_path)

        # 排序
        if sys.platform.startswith("win"):
            _strcmp = ctypes.windll.Shlwapi.StrCmpLogicalW
            def cmp(a, b):
                return _strcmp(str(a), str(b))
            image_paths.sort(key=functools.cmp_to_key(cmp))
        else:
            import re
            def natural_key(s):
                return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]
            image_paths.sort(key=lambda x: natural_key(os.path.basename(x)))

        if not image_paths:
            print(f"No valid images found in {folder}")
            return (False, None, None)
        
        images = []
        image_names = []

        # 加载图片
        for path in image_paths:
            try:
                img = Image.open(path).convert("RGB")
                img_array = np.array(img).astype(np.float32) / 255.0
                images.append(torch.from_numpy(img_array))

                # 提取不带后缀的名称
                base_name = os.path.splitext(os.path.basename(path))[0]
                image_names.append(base_name)

            except Exception as e:
                print(f"Error loading image {path}: {e}")
        
        if not images:
            print("No images could be loaded")
            return (False, None, None)
        
        # return (True, images, image_names)
        return (True, images, "\n".join(image_names))
