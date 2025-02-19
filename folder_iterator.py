import os
import random
from check import check
class FolderIteratorNODE:
    def __init__(self):
        self._current_index = 0  # 用于顺序模式和无限模式的迭代

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "base_path": ("STRING", {"default": "base_path"}), 
                "iterator_mode": (["sequential", "random", "Infinite"], {"default": "sequential"}),  
                "is_enable": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "BOOLEAN", "STRING", "BOOLEAN")  # 返回类型是字符串、布尔值
    RETURN_NAMES = ("path", "bool", "log", "is_end")  # 返回变量名
    FUNCTION = "iterate_folders"  # 执行的入口方法名称
    CATEGORY = "dong_tools/folder_iterator_by_dong"  # 分类，决定显示在哪一类节点下

    def iterate_folders(self, base_path, iterator_mode, is_enable):
        """
        根据传入的路径迭代子文件夹，忽略隐藏文件夹。
        :param base_path: 文件夹路径
        :param iterator_mode: 迭代模式，支持 "random", "Infinite", "sequential"（默认顺序模式）
        :param is_enable: 是否启用功能
        :return: 返回子文件夹路径、成功标志、日志信息、是否是文件夹最后一个
        """
        if not check():
            print("未授权用户")
            return ("", False, "未授权用户", False)
        if not is_enable:
            return ("", False, "功能已禁用", False)
        
        if not os.path.exists(base_path):
            return ("", False, "文件夹不存在", False)
        
        try:
            subfolders = [f for f in os.listdir(base_path) 
                          if os.path.isdir(os.path.join(base_path, f)) and not f.startswith('.')]
        except Exception as e:
            return ("", False, f"无法读取目录: {str(e)}", False)
        
        if not subfolders:
            return ("", False, "文件夹中无子文件夹", False)
    
        # 根据 iterator_mode 选择子文件夹
        try:
            if iterator_mode == "random":
                selected_folder = random.choice(subfolders)
                is_end = False 
            elif iterator_mode == "Infinite":
                # 无限模式：循环遍历所有文件夹
                selected_folder = subfolders[self._current_index % len(subfolders)]
                is_end = False  # 无限模式下永远不是最后一个
                self._current_index += 1
            else:  # 默认使用顺序模式
                selected_folder = subfolders[self._current_index]
                # 判断是否是最后一个子文件夹
                is_end = (self._current_index == len(subfolders) - 1)
                self._current_index = (self._current_index + 1) % len(subfolders)
    
            folder_path = os.path.join(base_path, selected_folder)
            folder_path = os.path.normpath(folder_path)  # 确保路径格式正确
            return (folder_path, True, "", is_end)  # 返回文件夹路径、成功标志、空日志、是否是文件夹中的最后一个子文件夹
    
        except Exception as e:
            return ("", False, f"发生错误: {str(e)}", False)  # 捕获异常并返回错误信息
            
    @classmethod
    def IS_CHANGED(cls, is_enable):
        return True
