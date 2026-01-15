import numpy as np
from PIL import Image
import torch

class 宫格图切分节点:
    CATEGORY = "dong_tools/AutoImageSplit_by_dong"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "split_image"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "图像": ("IMAGE",),
                "行": ("INT", {"default": 3, "min": 1}),
                "列": ("INT", {"default": 3, "min": 1}),
            }
        }

    def split_image(self, 图像, 行, 列):
        # IMAGE -> PIL
        img_tensor = 图像[0].cpu().numpy()
        img_array = np.clip(img_tensor * 255.0, 0, 255).astype(np.uint8)
        img = Image.fromarray(img_array)

        img_width, img_height = img.size

        tile_width = img_width // 列
        tile_height = img_height // 行

        output_images = []

        for row in range(行):
            for col in range(列):
                left = col * tile_width
                upper = row * tile_height
                right = left + tile_width
                lower = upper + tile_height

                tile = img.crop((left, upper, right, lower))

                tile_np = np.array(tile).astype(np.float32) / 255.0
                tile_tensor = torch.from_numpy(tile_np)[None, ...] 
                output_images.append(tile_tensor)

        return (torch.cat(output_images, dim=0),)