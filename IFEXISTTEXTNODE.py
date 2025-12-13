import os
from check import check

class IFEXISTTEXTNODE:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING",),
                "value": ("STRING",),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("bool",)
    FUNCTION = "process_text"
    CATEGORY = "dong_tools/text_utils_by_dong"

    def process_text(self, text, value, is_enable):
        # 功能开关
        if not is_enable:
            print("功能已禁用")
            return (False,)

        # 授权检查
        if not check():
            print("未授权用户")
            return (False,)

        # 判断 value 是否在 text 中
        if value in text:
            return (True,)
        else:
            return (False,)
