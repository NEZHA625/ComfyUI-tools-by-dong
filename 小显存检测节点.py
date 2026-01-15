import torch
import math
from check import check

class 小显存检测节点:

    @classmethod
    def INPUT_TYPES(s):
        return {}
    
    RETURN_TYPES = ("BOOLEAN",) 
    RETURN_NAMES = ("bool", )  
    FUNCTION = "checkvram" 
    CATEGORY = "dong_tools/is_small_vram_by_dong" 

    def checkvram(self):
        if not check():
            print("未授权用户")
            return (False,)

        # 显存检测（向上取整）
        if torch.cuda.is_available():
            vram_bytes = torch.cuda.get_device_properties(0).total_memory
            vram_gb = math.ceil(vram_bytes / (1024 ** 3))
            print(f"当前显存大小: {vram_gb} GB")

            return (vram_gb < 32,)
        else:
            print("未检测到GPU")
            return (False,)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return True
