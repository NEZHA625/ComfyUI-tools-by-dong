import os
from PIL import Image
import torch
import numpy as np
from check import check

class GetImageListFromFloderNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder": ("STRING",),  
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "IMAGE")  
    RETURN_NAMES = ("bool", "image") 
    FUNCTION = "process_images" 
    CATEGORY = "dong_tools/get_image_list_from_floder_by_dong" 

    def process_images(self, folder, is_enable):
        if not is_enable:
            print("功能已禁用")
            return (False, None)

        if not check():
            print("未授权用户")
            return (False, None)

        # Supported image extensions
        valid_extensions = {'.png', '.jpg', '.jpeg'}
        image_paths = []
        
        # Walk through the directory and find all valid images
        for root, _, files in os.walk(folder):
            for file in files:
                if os.path.splitext(file)[1].lower() in valid_extensions:
                    image_paths.append(os.path.join(root, file))
        
        if not image_paths:
            print(f"No valid images found in {folder}")
            return (False, None)
        
        # Load and process all images
        images = []
        for path in image_paths:
            try:
                img = Image.open(path).convert("RGB")
                img_array = np.array(img).astype(np.float32) / 255.0
                images.append(img_array)
            except Exception as e:
                print(f"Error loading image {path}: {e}")
        
        if not images:
            print("No images could be loaded")
            return (False, None)
        
        # Stack all images into a single tensor
        images_tensor = torch.from_numpy(np.stack(images))
        
        return (True, images_tensor)