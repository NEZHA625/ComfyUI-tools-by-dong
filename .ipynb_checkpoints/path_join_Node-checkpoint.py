import os
import time
from check import check
class path_join_Node:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
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

    def path_join(self, folder_path,file_name, is_make_dir, is_enable):
        if not check():
            print("未授权用户")
            return (False,)
        if not is_enable:
            print("功能已禁用")
            return (False,)  
            
        file_path = os.path.join(folder_path, file_name)    
        
        if not is_make_dir:   
            return(True,file_path)

        os.makedirs(file_path, exist_ok=True)

    @classmethod
    def IS_CHANGED(cls, folder_path,file_name, is_make_dir, is_enable):
        return True
