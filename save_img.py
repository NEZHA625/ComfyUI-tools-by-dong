import os
from torchvision import transforms
import torch
import re
from PIL import Image, PngImagePlugin
from check import check

class save_img_NODE:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "image_name": ("STRING",),
                "save_folder": ("STRING",{"default":"save_to_folder"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING", "BOOLEAN", "IMAGE")
    RETURN_NAMES = ("image_path", "success", "image")
    FUNCTION = "save_image"
    CATEGORY = "dong_tools/save_img_by_dong"

    def save_image(self, image, image_name, save_folder,is_enable):
        if not check():
            print("未授权用户")
            return (False,)
            
        if not is_enable:
            print("功能已禁用")
            return (False,)
            
        image_path = self.get_unique_image_path(save_folder, image_name)

        try:
            img = image
            image_single = img[0] 
            image_single = image_single.permute(2, 0, 1)
            to_pil = transforms.ToPILImage()
            img = to_pil(image_single)  
            if isinstance(img, Image.Image): 
                img.save(image_path)
                print(f"Image saved to {image_path}")
            else:
                img = Image.open(img)
                image_format = img.format
                print(f"图像格式: {image_format}")
                print("Provided image is not a valid PIL image.")
        except Exception as e:
            print(f"An error occurred while saving the image: {e}")
        else:
            pass
        return (image_path, True, image)
        
    def sanitize_file_name(self, file_name):
        """
        清理文件名中的非法字符，返回一个合法的文件名。
        """
        
        illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        
        sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', file_name)
        return sanitized_name
        
    def get_unique_image_path(self, save_path, image_name):
        
        image_name = self.sanitize_file_name(image_name)
        
        # 确保 image_name 以 .png 结尾
        if not image_name.endswith(".png"):
            image_name += ".png"

        # 如果文件夹路径不存在，创建它
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # 获取当前文件夹内所有以 base_name 开头的文件
        base_name, ext = os.path.splitext(image_name)
        existing_files = [f for f in os.listdir(save_path) if f.startswith(base_name) and f.endswith(ext)]
        
        # 如果没有现有文件，返回从01开始的文件名
        if not existing_files:
            return os.path.join(save_path, f"{base_name}_01{ext}")
        
        # 提取现有文件的编号
        existing_numbers = []
        for file in existing_files:
            # 提取文件名中的数字部分
            match = re.search(rf"{re.escape(base_name)}_(\d+)", file)
            if match:
                existing_numbers.append(int(match.group(1)))

        # 如果没有找到任何数字部分，直接返回 base_name_01.png
        if not existing_numbers:
            return os.path.join(save_path, f"{base_name}_01{ext}")

        # 找出缺失的数字
        all_numbers = set(range(1, max(existing_numbers) + 2))  # 包含最大值的下一个数字
        missing_numbers = list(all_numbers - set(existing_numbers))
        missing_numbers.sort()  # 排序

        # 如果存在缺失的数字，则返回第一个缺失的数字
        if missing_numbers:
            next_number = missing_numbers[0]
        else:
            # 如果没有缺失的数字，返回最大数字+1
            next_number = max(existing_numbers) + 1

        # 生成新的文件名
        image_name = f"{base_name}_{str(next_number).zfill(2)}{ext}"
        return os.path.join(save_path, image_name)

    @classmethod
    def IS_CHANGED(cls, image, image_name, save_folder,is_enable):
        return True