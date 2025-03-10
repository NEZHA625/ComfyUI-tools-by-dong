import os
from check import check

class find_files_by_extension_Node:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "folder_path": ("STRING", {"default": "path"}), 
                "file_extension": (["png", "json", "safetensors", "pth", "jpg", "jpeg", "yaml"], {"default": "png"}),  
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "LIST", "STRING","STRING")  
    RETURN_NAMES = ("bool", "file_list", "first_file","floder") 
    FUNCTION = "find_files_by_extension" 
    CATEGORY = "dong_tools/find_files_by_extension_by_dong" 

    def find_files_by_extension(self, folder_path, file_extension, is_enable):
        
        if not check():
            print("未授权用户")
            return (False, [], "")
            
        if not is_enable:
            return (False, [], "")

        if not os.path.exists(folder_path):
            return (False, [], "")
        
        result = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(file_extension):
                    absolute_path = os.path.join(root, file)
                    result.append(absolute_path)
        
        result.sort()
        
        if result:
            return (True, result, result[0],folder_path)
        else:
            return (False, [], "", "")
