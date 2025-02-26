import os
import random
import torch
from comfy.utils import load_torch_file
from comfy.sd import load_lora_for_models

class LoraIterator:
    def __init__(self):
        self.index = 0
        self.path = None
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {"default": ""}),
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "is_enable": ("BOOLEAN", {"default": True}),
                "is_reload": ("BOOLEAN", {"default": False}),
                "iterator_mode": (["sequential", "random", "Infinite"], {"default": "sequential"}),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "BOOLEAN","STRING","STRING")
    RETURN_NAMES = ("model", "clip", "lora_name", "is_end","lora_absolute_path","loras_path")

    CATEGORY = "dong_tools/LoRA_Iterators"

    # 定义主要逻辑方法，供 FUNCTION 使用
    def file(self, folder_path, model, clip, iterator_mode, strength_model=1.0, strength_clip=1.0, is_enable=True, is_reload=False):
        if not is_enable:
            return model, clip, "No LoRA", False

        # 如果路径变更或重新加载标志被设置，则重置索引
        if self.path != folder_path or is_reload:
            self.index = 0
            self.path = folder_path

        try:
            # 查找文件夹中的有效文件，并按修改时间排序
            lora_files = sorted(
                [f for f in os.listdir(folder_path) if f.lower().endswith((".pt", ".safetensors"))],
                key=lambda f: os.path.getmtime(os.path.join(folder_path, f))
            )
        except FileNotFoundError:
            raise ValueError(f"Folder path '{folder_path}' does not exist.")

        if not lora_files:
            raise ValueError("No valid LoRA files found in the folder.")

        if self.index >= len(lora_files):
            # 对于顺序模式，到达末尾时返回结束标志
            if iterator_mode == "sequential":
                return model, clip, "End of Lora", True ,lora_absolute_path, loras_path
            self.index = 0  # 重置索引用于无限模式

        # 获取当前文件路径和名称
        lora_name = lora_files[self.index]
        lora_path = os.path.join(folder_path, lora_name)
        lora_absolute_path = lora_path
        loras_path = folder_path

        # 检查并从缓存加载LoRA
        if self.loaded_lora and self.loaded_lora[0] == lora_path:
            lora = self.loaded_lora[1]
        else:
            lora = load_torch_file(lora_path, safe_load=True)
            self.loaded_lora = (lora_path, lora)

        # 应用LoRA到模型和CLIP
        model_lora, clip_lora = load_lora_for_models(model, clip, lora, strength_model, strength_clip)

        # 根据迭代模式更新索引
        is_end = False
        if iterator_mode == "sequential":
            self.index += 1
            is_end = self.index >= len(lora_files)
        elif iterator_mode == "random":
            self.index = random.randint(0, len(lora_files) - 1)
        elif iterator_mode == "Infinite":
            self.index = (self.index + 1) % len(lora_files)

        # 返回更新后的模型、CLIP和当前LoRA名称
        return model_lora, clip_lora, os.path.splitext(lora_name)[0], is_end,lora_absolute_path,loras_path

    # 定义 FUNCTION 属性，指向 file 方法
    FUNCTION = "file"

    @classmethod
    def IS_CHANGED(cls):
        return True
    

