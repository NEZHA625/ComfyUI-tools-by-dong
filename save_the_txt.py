import os
import time
import re  
from check import check

class SaveTXTNode:

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
                "save_target_path": ("STRING", {"default": "target_floder"}),               
                "file_name": ("STRING", {"default": "file_name"}),          
                "is_enable": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)  
    RETURN_NAMES = ("bool",)  
    FUNCTION = "SaveTXT" 
    CATEGORY = "dong_tools/Save_text_by_dong" 

    def sanitize_file_name(self, file_name):
        """
        清理文件名中的非法字符，返回一个合法的文件名。
        """
        
        illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        
        sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', file_name)
        return sanitized_name

    def SaveTXT(self, text, save_target_path, file_name, is_enable):
        time.sleep(1)  
        if not check():
            print("未授权用户")
            return (False,)
        if not is_enable:
            print("功能已禁用")
            return (False,)  
    
        # 确保目标路径存在
        if not os.path.exists(save_target_path):
            os.makedirs(save_target_path)
        
        # 清理文件名中的非法字符
        file_name = self.sanitize_file_name(file_name)

        # 拼接文件完整路径
        if not file_name.endswith(".txt"):
            file_path = os.path.join(save_target_path, f"{file_name}.txt")
        else:
            file_path = os.path.join(save_target_path, file_name)
        
        try:
            # 将文本保存到指定文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"文件已保存至 {file_path}")
            return (True,) 
        except Exception as e:
            print(f"保存文件时出错: {e}")
            return (False,)  
