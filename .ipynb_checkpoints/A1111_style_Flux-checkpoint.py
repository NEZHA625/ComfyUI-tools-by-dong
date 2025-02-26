from torchvision import transforms
import torch
from PIL import Image, PngImagePlugin
import os


class A1111_FLUX_DATA_NODE:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_image_absolute_path": ("STRING", {"default": "input_image_absolute_path"}),
                "save_image_absolute_path": ("STRING", {"default": "save_image_absolute_path"}),
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
                "is_enable": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "Lora_hash": ("STRING", {"default": "d143db10789e"}),
                "Lora_name": ("STRING", {"default": "F.1_lora"}),
            }
        }

    RETURN_TYPES = ("STRING", "BOOLEAN")
    RETURN_NAMES = ("save_image_absolute_path", "success")
    FUNCTION = "process_image"
    CATEGORY = "dong_tools/A1111_FLUX_data_by_dong"

    def process_image(self, input_image_absolute_path, save_image_absolute_path, prompt, steps, sampler_name, Schedule_type, cfg_scale,
                     Distilled_CFG_Scale, seeds, width, height, sd_model_hash, sd_model_name, Module_1, Module_2, Module_3, is_enable,
                     Lora_hash=None, Lora_name=None):

        if not is_enable:
            print("功能已禁用")
            return (False,)

        params = {
            "input_image_absolute_path": input_image_absolute_path,
            "save_image_absolute_path": save_image_absolute_path,
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
            "is_enable": is_enable,
            "Lora_hash": Lora_hash,
            "Lora_name": Lora_name
        }

        filename_gen = PhotoINFOGenerator()
        generated_info = filename_gen.generate_info(params)
        PhotoINFOGenerator.add_info_to_png(input_image_absolute_path, generated_info, save_image_absolute_path)

        return save_image_absolute_path, True

    @classmethod
    def IS_CHANGED(self, input_image_absolute_path, save_image_absolute_path, prompt, steps, sampler_name, Schedule_type, cfg_scale,
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
    def add_info_to_png(image_path: str, info: str, output_path: str):
        try:
            image = Image.open(image_path)
            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", info)
            image.save(output_path, pnginfo=pnginfo)
            image.close()
        except FileNotFoundError:
            print(f"Image not found at {image_path}")
            raise
        except Exception as e:
            print(f"Error saving image: {e}")
            raise