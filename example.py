import os
import time
class exampleNode:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "": ("STRING", {"default": "source_directory"}), 
                "": ("STRING", {"default": "new_name"}),  
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN","STRING")  
    RETURN_NAMES = ("bool","text") 
    FUNCTION = "example" 
    CATEGORY = "dong_tools/example_by_dong" 

    def example(self, ,, is_enable):
        
        if not is_enable:
            print("功能已禁用")
            return (False,)  

