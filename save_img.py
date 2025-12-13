import os
from torchvision import transforms
import torch
import re
from PIL import Image
from check import check

class save_img_NODE:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "image_name": ("STRING",),
                "save_folder": ("STRING", {"default": "save_to_folder"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    # 返回 4 个类型
    RETURN_TYPES = ("STRING", "STRING", "BOOLEAN", "IMAGE")
    RETURN_NAMES = ("image_path", "final_image_name", "success", "image")
    FUNCTION = "save_image"
    CATEGORY = "dong_tools/save_img_by_dong"

    # -------------------------
    # 主函数：保存图像
    # -------------------------
    def save_image(self, image, image_name, save_folder, is_enable):
        if not check():
            print("未授权用户")
            return ("", "", False, image)

        if not is_enable:
            print("功能已禁用")
            return ("", "", False, image)

        # 获取唯一文件路径 + 自动编号后的文件名
        image_path, final_image_name = self.get_unique_image_path(save_folder, image_name)

        try:
            image_single = image[0]
            image_single = image_single.permute(2, 0, 1)

            to_pil = transforms.ToPILImage()
            img = to_pil(image_single)

            if isinstance(img, Image.Image):
                img.save(image_path)
                print(f"Image saved to {image_path}")
            else:
                print("不是有效的 PIL 图像")
                return ("", "", False, image)

        except Exception as e:
            print(f"保存图像发生错误: {e}")
            return ("", "", False, image)

        return (image_path, final_image_name, True, image)

    # -------------------------
    # 清理非法字符
    # -------------------------
    def sanitize_file_name(self, file_name):
        sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', file_name)
        return sanitized_name

    # -------------------------
    # 自动编号文件名 & 路径
    # -------------------------
    def get_unique_image_path(self, save_path, image_name):

        image_name = self.sanitize_file_name(image_name)

        if not image_name.endswith(".png"):
            image_name += ".png"

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        base_name, ext = os.path.splitext(image_name)
        existing_files = [
            f for f in os.listdir(save_path)
            if f.startswith(base_name) and f.endswith(ext)
        ]

        # 没有则从 _01 开始
        if not existing_files:
            final_name = f"{base_name}_01{ext}"
            return os.path.join(save_path, final_name), final_name

        # 提取数字
        numbers = []
        for file in existing_files:
            match = re.search(rf"{re.escape(base_name)}_(\d+)", file)
            if match:
                numbers.append(int(match.group(1)))

        if not numbers:
            final_name = f"{base_name}_01{ext}"
            return os.path.join(save_path, final_name), final_name

        # 查找缺失的编号
        all_numbers = set(range(1, max(numbers) + 2))
        missing = sorted(all_numbers - set(numbers))

        if missing:
            next_number = missing[0]
        else:
            next_number = max(numbers) + 1

        final_name = f"{base_name}_{str(next_number).zfill(2)}{ext}"
        return os.path.join(save_path, final_name), final_name

    @classmethod
    def IS_CHANGED(cls, image, image_name, save_folder, is_enable):
        return True
