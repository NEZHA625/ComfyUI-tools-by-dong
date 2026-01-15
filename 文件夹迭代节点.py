import os
import random
from check import check

class 文件夹迭代节点:
    def __init__(self):
        self._current_index = 0  # 用于顺序模式和无限模式的迭代

    @classmethod
    def INPUT_TYPES(cls):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "工作路径": ("STRING",), 
                "迭代模式": (["顺序", "随机", "无限"], {"default": "顺序"}),  
                "节点开关": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "BOOLEAN", "STRING", "BOOLEAN")  
    RETURN_NAMES = ("path", "bool", "log", "is_end")  
    FUNCTION = "iterate_folders"
    CATEGORY = "dong_tools/folder_iterator_by_dong" 

    def iterate_folders(self, 工作路径, 迭代模式, 节点开关):
        
        if not check():
            print("未授权用户")
            return ("", False, "未授权用户", False)
            
        if not 节点开关:
            return ("", False, "功能已禁用", False)
        
        if not os.path.exists(工作路径):
            return ("", False, "文件夹不存在", False)
        
        try:
            子文件夹列表 = [f for f in os.listdir(工作路径) 
                          if os.path.isdir(os.path.join(工作路径, f)) and not f.startswith('.')]
        except Exception as e:
            return ("", False, f"无法读取目录: {str(e)}", False)
        
        if not 子文件夹列表:
            return ("", False, "文件夹中无子文件夹", False)
    
        try:
            if 迭代模式 == "随机":
                selected_folder = random.choice(子文件夹列表)
                is_end = False 
            elif 迭代模式 == "无限":
                selected_folder = 子文件夹列表[self._current_index % len(子文件夹列表)]
                is_end = False
                self._current_index += 1
            else:  # 默认顺序模式
                selected_folder = 子文件夹列表[self._current_index]
                is_end = (self._current_index == len(子文件夹列表) - 1)
                self._current_index = (self._current_index + 1) % len(子文件夹列表)
    
            folder_path = os.path.join(工作路径, selected_folder)
            folder_path = os.path.normpath(folder_path)
            return (folder_path, True, "", is_end)
    
        except Exception as e:
            return ("", False, f"发生错误: {str(e)}", False)
        
    @classmethod
    def IS_CHANGED(cls, 节点开关):
        return True
