import os
import time
import re
from check import check
class path_join_Node:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder_path": ("STRING", {"default": "path"}),  
                "file_name": ("STRING", {"default": "new_name"}),
                "is_make_dir": ("BOOLEAN", {"default": False}),
                "is_enable": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("BOOLEAN","STRING")  # 返回类型是布尔值
    RETURN_NAMES = ("bool","file_path")  # 返回变量名是bool
    FUNCTION = "path_join"  # 执行的入口方法
    CATEGORY = "dong_tools/path_join_by_dong"  # 分类，决定显示在哪一类节点下
    
    def sanitize_file_name(self, file_name):
        """
        清理文件名中的非法字符，返回一个合法的文件名。
        """
        
        illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        
        sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', file_name)
        return sanitized_name
        
    def path_join(self, folder_path,file_name, is_make_dir, is_enable):
        if not check():
            print("未授权用户")
            return (False,)
        if not is_enable:
            print("功能已禁用")
            return (False,)  
            
        file_name = self.sanitize_file_name(file_name)  
        
        file_path = os.path.join(folder_path, file_name)    
        
        if not is_make_dir:   
            return(True,file_path)
        else:
            os.makedirs(file_path)
            return(True,file_path)

    @classmethod
    def IS_CHANGED(cls, folder_path,file_name, is_make_dir, is_enable):
        return True
