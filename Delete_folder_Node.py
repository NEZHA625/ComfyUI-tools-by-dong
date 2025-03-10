import os
import shutil
from check import check

class Delete_folder_Node:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "path": ("STRING", {"default": "path"}), 
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)  
    RETURN_NAMES = ("bool",) 
    FUNCTION = "Delete_folder" 
    CATEGORY = "dong_tools/Delete_by_dong" 

    def Delete_folder(self, path, is_enable):
        if not check():
            print("未授权用户")
            return (False,)
        if not is_enable:
            print("功能已禁用")
            return (False,) 

        # 检查文件或文件夹是否存在
        if not os.path.exists(path):
            print(f"文件或文件夹 {path} 不存在")
            return (False,)

        # 尝试删除文件或文件夹
        try:
            if os.path.isdir(path):  # 如果是文件夹
                shutil.rmtree(path)  # 删除非空文件夹
                print(f"文件夹 {path} 已成功删除")
            elif os.path.isfile(path):  # 如果是文件
                os.remove(path)  # 删除文件
                print(f"文件 {path} 已成功删除")
            return (True,)
        except Exception as e:
            print(f"删除操作失败: {e}")
            return (False,)
