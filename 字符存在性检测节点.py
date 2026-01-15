import os
class 字符存在性检测节点:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "字符串": ("STRING",),
                "目标值": ("STRING",),
                "is_enable": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("bool",)
    FUNCTION = "process_text"
    CATEGORY = "dong_tools/text_detect_by_dong"

    def process_text(self, 字符串, 目标值, is_enable):
        if not is_enable:
            print("功能已禁用")
            return (False,)

        if 目标值 in 字符串:
            return (True,)
        else:
            return (False,)
