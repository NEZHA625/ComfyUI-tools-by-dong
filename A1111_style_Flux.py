import os
from torchvision import transforms
import torch
import re
from PIL import Image, PngImagePlugin

from check import check

class A1111_FLUX_DATA_NODE:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "image_name": ("STRING",),
                "save_path": ("STRING", {"default": "D:\\mnt\\workspace\\ComfyUI\\output\\a1111_data"}),
                "prompt": ("STRING", {"default": "1girl"}),
                "steps": ("INT", {"default": 20}),
                "sampler_name": ("STRING", {"default": "Euler"}),
                "Schedule_type": ("STRING", {"default": "Simple"}),
                "cfg_scale": ("FLOAT", {"default": 1.0}),
                "Distilled_CFG_Scale": ("FLOAT", {"default": 3.5}),
                "seeds": ("INT", {"default": 3825474120}),
                "width": ("INT", {"default": 960}),
                "height": ("INT", {"default": 1280}),
                "sd_model_hash": ("STRING", {"default": "275ef623d3"}),
                "sd_model_name": ("STRING", {"default": "flux1-dev-fp8"}),
                "Module_1": ("STRING", {"default": "clip_l"}),
                "Module_2": ("STRING", {"default": "t5xxl_fp16"}),
                "Module_3": ("STRING", {"default": "ae"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "Lora_hash": ("STRING", {"default": "F1_lora"}),
                "Lora_name": ("STRING", {"default": "F1_lora"}),
            }
        }

    RETURN_TYPES = ("STRING", "BOOLEAN", "IMAGE")
    RETURN_NAMES = ("image_path", "success", "image")
    FUNCTION = "process_image"
    CATEGORY = "dong_tools/A1111_FLUX_data_by_dong"

    def process_image(self, image, image_name, save_path, prompt, steps, sampler_name, Schedule_type, cfg_scale,
                     Distilled_CFG_Scale, seeds, width, height, sd_model_hash, sd_model_name, Module_1, Module_2, Module_3, is_enable,
                     Lora_hash=None, Lora_name=None):
        if not check():
            print("未授权用户")
            return (False,)
            
        if not is_enable:
            print("功能已禁用")
            return (False,)

        # 调整维度并转换为 PIL 图像
        image_single = image[0]  # 选择第一张图像，形状为 (H, W, C)
        image_single = image_single.permute(2, 0, 1)  # 转换为 (C, H, W)
        to_pil = transforms.ToPILImage()
        pil_image = to_pil(image_single)  # 转换为 PIL 图像

        # 生成参数并保存图像
        params = {
            "image": pil_image,
            "prompt": prompt,
            "steps": steps,
            "sampler_name": sampler_name,
            "Schedule_type": Schedule_type,
            "cfg_scale": cfg_scale,
            "Distilled_CFG_Scale": Distilled_CFG_Scale,
            "seeds": seeds,
            "width": width,
            "height": height,
            "sd_model_hash": sd_model_hash,
            "sd_model_name": sd_model_name,
            "Module_1": Module_1,
            "Module_2": Module_2,
            "Module_3": Module_3,
            "Lora_hash": Lora_hash,
            "Lora_name": Lora_name
        }

        filename_gen = PhotoINFOGenerator()
        generated_info = filename_gen.generate_info(params)

        # 生成唯一的文件路径
        image_path = self.get_unique_image_path(save_path, image_name)

        # 将信息添加到 PNG 中
        PhotoINFOGenerator.add_info_to_png(pil_image, generated_info, image_path)

        return image_path, True, image

    def get_unique_image_path(self, save_path, image_name):
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
    def IS_CHANGED(cls, image, image_name, save_path, prompt, steps, sampler_name, Schedule_type, cfg_scale,
                     Distilled_CFG_Scale, seeds, width, height, sd_model_hash, sd_model_name, Module_1, Module_2, Module_3, is_enable,
                     Lora_hash=None, Lora_name=None):
        return True


class PhotoINFOGenerator:
    def generate_info(self, params):
        replacements = {
            'Prompt': lambda p: p['prompt'],
            'Steps': lambda p: p['steps'],
            'Sampler': lambda p: p['sampler_name'],
            'Schedule type': lambda p: p['Schedule_type'],
            'CFG scale': lambda p: p['cfg_scale'],
            'Distilled CFG Scale': lambda p: p['Distilled_CFG_Scale'],
            'Seed': lambda p: p['seeds'],
            'Size': lambda p: f"{p['width']}x{p['height']}",
            'Model hash': lambda p: p['sd_model_hash'],
            'Model': lambda p: p['sd_model_name'],
            'Lora hashes': lambda p: f'"{p.get("Lora_name")}: {p.get("Lora_hash")}"' if p.get('Lora_name') and p.get('Lora_hash') else None,
            'Version': lambda p: 'f2.0.1v1.10.1-previous-635-gf5330788',
            'Module 1': lambda p: 'clip_l',
            'Module 2': lambda p: 't5xxl_fp16',
            'Module 3': lambda p: 'ae',
        }
        info_parts = []
        other_parts = []
        for key, func in replacements.items():
            value = func(params)
            if key == 'Prompt':
                info_parts.append(value)
            elif key == 'Lora hashes' and value is None:
                continue  # 当 key 为 'Lora hashes' 且 value 为 None 时，跳过当前迭代
            else:
                other_parts.append(f"{key}: {value}")
        return "\n".join(info_parts) + "\n" + ", ".join(other_parts)

    @staticmethod
    def add_info_to_png(image, info: str, output_path: str):
        try:
            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", info)
            image.save(output_path, pnginfo=pnginfo)
            image.close()
        except FileNotFoundError:
            print(f"Image not found at {output_path}")
            raise
        except Exception as e:
            print(f"Error saving image: {e}")
            raise
