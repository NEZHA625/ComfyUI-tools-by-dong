import os
from torchvision import transforms
import torch
from PIL import Image
from check import check

class save_img_v2_NODE:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "image_name": ("STRING",),
                "formate": ("STRING",),
                "save_folder": ("STRING",),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING", "BOOLEAN", "IMAGE")
    RETURN_NAMES = ("image_path", "success", "image")
    FUNCTION = "save_image_v2"
    CATEGORY = "dong_tools/save_img_v2_by_dong"

    def save_image_v2(self, image, image_name, formate, save_folder, is_enable):
        if not check():
            print("未授权用户")
            return (False, False, None)
        
        if not is_enable:
            print("功能已禁用")
            return (False, False, None)

        # 创建保存文件夹
        os.makedirs(save_folder, exist_ok=True)

        # 根据 formate 生成文件名
        if formate.endswith("_"):
            filename = f"{formate}{image_name}.png"
        elif formate.startswith("_"):
            filename = f"{image_name}{formate}.png"
        else:
            filename = f"{image_name}_{formate}.png"

        image_path = os.path.join(save_folder, filename)

        try:
            img_tensor = image[0]  # 取 batch 中的第一张
            img_tensor = img_tensor.permute(2, 0, 1)  # 转换维度
            to_pil = transforms.ToPILImage()
            img = to_pil(img_tensor)
            img.save(image_path)
            print(f"Image saved to {image_path}")
        except Exception as e:
            print(f"保存图像时出错: {e}")
            return (image_path, False, image)

        return (image_path, True, image)

    @classmethod
    def IS_CHANGED(cls, image, image_name, formate, save_folder, is_enable):
        return True
