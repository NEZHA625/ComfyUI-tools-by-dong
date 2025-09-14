import os
from PIL import Image
import numpy as np
import torch

class GetRefModelImageListNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ref_image_path": ("STRING",),
                "model_image_path": ("STRING",),
            }
        }

    RETURN_TYPES = ("BOOLEAN","IMAGE","IMAGE","STRING","STRING")
    RETURN_NAMES = ("bool","ref_image_list","model_image_list","image_save_name_list","ref_image_path_list")
    FUNCTION = "get_image_list"
    CATEGORY = "dong_tools/for_by_dong"

    def get_image_list(self, ref_image_path, model_image_path):
        ref_image_list = []
        model_image_list = []
        image_save_name_list = []
        ref_image_path_list = []

        print(f"[INFO] 开始扫描 ref_image_path: {ref_image_path}")
        print(f"[INFO] 开始扫描 model_image_path: {model_image_path}")

        # 获取一级子文件夹
        ref_folders = [f for f in os.listdir(ref_image_path) if os.path.isdir(os.path.join(ref_image_path, f))]
        model_folders = [f for f in os.listdir(model_image_path) if os.path.isdir(os.path.join(model_image_path, f))]

        print(f"[INFO] ref 文件夹下一级子文件夹: {ref_folders}")
        print(f"[INFO] model 文件夹下一级子文件夹: {model_folders}")

        # 匹配同名文件夹
        matched_folders = set(ref_folders) & set(model_folders)
        print(f"[INFO] 匹配到的同名文件夹: {matched_folders}")

        if not matched_folders:
            print("[ERROR] 没有匹配到任何同名文件夹")
            return False, [], [], [], []

        valid_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.webp'}

        for folder in matched_folders:
            print(f"[INFO] 处理文件夹: {folder}")
            ref_folder_path = os.path.join(ref_image_path, folder)
            model_folder_path = os.path.join(model_image_path, folder)

            # 读取 ref 图片
            ref_images_paths = [os.path.join(ref_folder_path, img) for img in os.listdir(ref_folder_path)
                                if os.path.isfile(os.path.join(ref_folder_path, img)) and os.path.splitext(img)[1].lower() in valid_extensions]

            print(f"[INFO] {folder} 下 ref 图片数量: {len(ref_images_paths)} -> {ref_images_paths}")

            if len(ref_images_paths) != 1:
                print(f"[ERROR] 文件夹 {folder} 下 ref 图片不止一张，返回 False")
                return False, [], [], [], []

            # 读取 model 子文件夹的所有子文件夹图片
            model_subfolders = [os.path.join(model_folder_path, sf) for sf in os.listdir(model_folder_path)
                                if os.path.isdir(os.path.join(model_folder_path, sf))]

            print(f"[INFO] {folder} 下 model 子文件夹: {[os.path.basename(sf) for sf in model_subfolders]}")

            for subfolder in model_subfolders:
                subfolder_name = os.path.basename(subfolder)
                model_images_paths = [os.path.join(subfolder, img) for img in os.listdir(subfolder)
                                      if os.path.isfile(os.path.join(subfolder, img)) and os.path.splitext(img)[1].lower() in valid_extensions]

                print(f"[INFO] 子文件夹 {subfolder_name} 下图片数量: {len(model_images_paths)} -> {model_images_paths}")

                # 加载 model 图片
                for p in model_images_paths:
                    try:
                        img = Image.open(p).convert("RGB")
                        img_array = np.array(img).astype(np.float32) / 255.0  # HWC
                        model_image_list.append(torch.from_numpy(img_array))
                        image_save_name_list.append(subfolder_name)
                    except Exception as e:
                        print(f"[ERROR] 加载 model 图片 {p} 出错: {e}")

                # 将对应的 ref 图片复制到和 model 子文件夹图片数量一致，同时记录文件夹绝对路径
                for p in ref_images_paths:
                    try:
                        img = Image.open(p).convert("RGB")
                        img_array = np.array(img).astype(np.float32) / 255.0  # HWC
                        for _ in model_images_paths:
                            ref_image_list.append(torch.from_numpy(img_array))
                            ref_image_path_list.append(os.path.abspath(ref_folder_path))
                    except Exception as e:
                        print(f"[ERROR] 加载 ref 图片 {p} 出错: {e}")
                        return False, [], [], [], []

        print(f"[INFO] 最终 ref_image_list 数量: {len(ref_image_list)}")
        print(f"[INFO] 最终 model_image_list 数量: {len(model_image_list)}")
        print(f"[INFO] 最终 image_save_name_list 数量: {len(image_save_name_list)}")
        print(f"[INFO] 最终 ref_image_path_list 数量: {len(ref_image_path_list)}")

        return (True, ref_image_list, model_image_list, image_save_name_list, ref_image_path_list)
