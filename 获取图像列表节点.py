import os
from PIL import Image
import torch
import numpy as np
from check import check
import sys
import ctypes
import functools

class 获取图像列表节点:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "文件夹": ("STRING",),  
                "节点开关": ("BOOLEAN", {"default": True}),
                "递归子文件夹": ("BOOLEAN", {"default": False}),  
            }
        }

    RETURN_TYPES = ("BOOLEAN", "IMAGE", "STRING")  
    RETURN_NAMES = ("状态", "图像列表", "名称列表") 
    FUNCTION = "处理图像" 
    CATEGORY = "dong_tools/get_image_list_by_dong" 

    def 处理图像(self, 文件夹, 节点开关, 递归子文件夹):
        if not 节点开关:
            print("功能已禁用")
            return (False, None, None)

        if not check():
            print("未授权用户")
            return (False, None, None)

        有效后缀 = {'.png', '.jpg', '.jpeg', '.webp'}
        图像路径列表 = []

        # 扫描文件夹
        if 递归子文件夹:
            for 根目录, _, 文件列表 in os.walk(文件夹):
                for 文件 in 文件列表:
                    if os.path.splitext(文件)[1].lower() in 有效后缀:
                        图像路径列表.append(os.path.join(根目录, 文件))
        else:
            for 文件 in os.listdir(文件夹):
                全路径 = os.path.join(文件夹, 文件)
                if os.path.isfile(全路径) and os.path.splitext(文件)[1].lower() in 有效后缀:
                    图像路径列表.append(全路径)

        # 排序
        if sys.platform.startswith("win"):
            _strcmp = ctypes.windll.Shlwapi.StrCmpLogicalW
            def cmp(a, b):
                return _strcmp(str(a), str(b))
            图像路径列表.sort(key=functools.cmp_to_key(cmp))
        else:
            import re
            def natural_key(s):
                return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]
            图像路径列表.sort(key=lambda x: natural_key(os.path.basename(x)))

        if not 图像路径列表:
            print(f"No valid images found in {文件夹}")
            return (False, None, None)
        
        图像列表 = []
        名称列表 = []

        # 加载图片
        for 路径 in 图像路径列表:
            try:
                图像 = Image.open(路径).convert("RGB")
                图像数组 = np.array(图像).astype(np.float32) / 255.0
                图像列表.append(torch.from_numpy(图像数组))

                # 提取不带后缀的名称
                基础名称 = os.path.splitext(os.path.basename(路径))[0]
                名称列表.append(基础名称)

            except Exception as e:
                print(f"Error loading image {路径}: {e}")
        
        if not 图像列表:
            print("No images could be loaded")
            return (False, None, None)
        
        return (True, 图像列表, "\n".join(名称列表))
