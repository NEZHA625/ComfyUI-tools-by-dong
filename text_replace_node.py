import os
from check import check

class text_replace_node:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "text": ("STRING", {"default": "text"}), 
                "From":("STRING", {"default": "from"}),
                "To":("STRING", {"default": "to"}),
                "is_enable": ("BOOLEAN", {"default": True}),  
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")
    RETURN_NAMES = ("bool", "text")
    FUNCTION = "text_replace"
    CATEGORY = "dong_tools/text_replace_by_dong"

    def text_replace(self, text, From, To, is_enable):
        if not check():
            print("未授权用户")
            return (False, "")
            
        if not is_enable:
            print("功能已禁用")
            return (False, "")  

        replaced_text = text.replace(From, To)
        return (True, replaced_text)