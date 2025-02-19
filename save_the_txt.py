import os
import time
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
                "save_target_path": ("STRING", {"default": "target_path"}),               
                "file_name": ("STRING", {"default": "file_name"}),          
                "is_enable": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)  # 返回类型是布尔值
    RETURN_NAMES = ("bool",)  # 返回变量名是bool
    FUNCTION = "SaveTXT"  # 执行的入口方法
    CATEGORY = "dong_tools/Save_text_by_dong"  # 分类，决定显示在哪一类节点下

    def SaveTXT(self, text, save_target_path, file_name, is_enable):
        time.sleep(3)  # 模拟延迟
        if not check():
            print("未授权用户")
            return (False,)
        if not is_enable:
            print("功能已禁用")
            return (False,)  # 如果禁用，则返回 False
    
        # 确保目标路径存在
        os.makedirs(save_target_path, exist_ok=True)
        
        # 拼接文件完整路径
        file_path = os.path.join(save_target_path, f"{file_name}.txt")
        
        try:
            # 将文本保存到指定文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"文件已保存至 {file_path}")
            return (True,)  # 成功保存返回 True
        except Exception as e:
            print(f"保存文件时出错: {e}")
            return (False,)  # 出错时返回 False

