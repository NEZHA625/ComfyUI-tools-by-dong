import os
import re
from torchvision import transforms
from PIL import Image
from check import check


class 保存图像节点:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "image_name": ("STRING",),
                "save_folder": ("STRING",),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "BOOLEAN", "IMAGE")
    RETURN_NAMES = ("image_path", "final_image_name", "success", "image")
    FUNCTION = "save_image"
    CATEGORY = "dong_tools/save_img_by_dong"

    def save_image(self, image, image_name, save_folder, is_enable):
        if not check():
            print("未授权用户")
            return ("", "", False, image)

        if not is_enable:
            print("功能已禁用")
            return ("", "", False, image)

        saved_paths = []
        saved_names = []

        try:
            batch_size = image.shape[0]
            to_pil = transforms.ToPILImage()

            for i in range(batch_size):
                image_path, final_image_name = self.get_unique_image_path(
                    save_folder,
                    image_name
                )

                image_single = image[i].permute(2, 0, 1)
                img = to_pil(image_single)

                if not isinstance(img, Image.Image):
                    print(f"第 {i} 张不是有效的 PIL 图像，已跳过")
                    continue

                img.save(image_path)
                print(f"Image saved to {image_path}")

                saved_paths.append(image_path)
                saved_names.append(final_image_name)

        except Exception as e:
            print(f"保存图像发生错误: {e}")
            return ("", "", False, image)

        if not saved_paths:
            return ("", "", False, image)

        return (
            "\n".join(saved_paths),
            "\n".join(saved_names),
            True,
            image
        )

    # -------------------------
    # 清理非法字符
    # -------------------------
    def sanitize_file_name(self, file_name):
        return re.sub(r'[<>:"/\\|?*]', '_', file_name)

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

        if not existing_files:
            final_name = f"{base_name}{ext}"
            return os.path.join(save_path, final_name), final_name

        numbers = []
        pattern = re.compile(rf"{re.escape(base_name)}_(\d+){re.escape(ext)}")
        for file in existing_files:
            match = pattern.match(file)
            if match:
                numbers.append(int(match.group(1)))

        if not numbers:
            next_number = 1
        else:
            all_numbers = set(range(1, max(numbers) + 2))
            missing = sorted(all_numbers - set(numbers))
            next_number = missing[0]

        final_name = f"{base_name}_{str(next_number).zfill(2)}{ext}"
        return os.path.join(save_path, final_name), final_name

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return True
