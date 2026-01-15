import os
import time
import re  
from check import check

class 保存文本节点:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "文本内容": ("STRING", {"default": "text"}),  
                "目标文件夹路径": ("STRING", {"default": "target_folder"}),               
                "自定义文件名": ("STRING", {"default": "file_name"}),          
                "节点开关": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)  
    RETURN_NAMES = ("状态",)  
    FUNCTION = "SaveTXT" 
    CATEGORY = "dong_tools/Save_text_by_dong" 

    def 清理文件名(self, 文件名):
        """
        清理文件名中的非法字符，返回一个合法的文件名。
        """
        # Windows 文件名非法字符
        非法字符列表 = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        合法文件名 = re.sub(r'[<>:"/\\|?*]', '_', 文件名)
        return 合法文件名

    def SaveTXT(self, 文本内容, 目标文件夹路径, 自定义文件名, 节点开关):
        time.sleep(1)  
        日志前缀 = "[保存TXT节点]"

        if not check():
            print(f"{日志前缀} 未授权用户")
            return (False,)
        if not 节点开关:
            print(f"{日志前缀} 功能已禁用")
            return (False,)  
    
        # 确保目标文件夹存在
        if not os.path.exists(目标文件夹路径):
            os.makedirs(目标文件夹路径)
        
        # 清理文件名中的非法字符
        自定义文件名 = self.清理文件名(自定义文件名)

        # 拼接完整文件路径
        if not 自定义文件名.endswith(".txt"):
            文件完整路径 = os.path.join(目标文件夹路径, f"{自定义文件名}.txt")
        else:
            文件完整路径 = os.path.join(目标文件夹路径, 自定义文件名)
        
        try:
            # 将文本保存到指定文件
            with open(文件完整路径, 'w', encoding='utf-8') as 文件:
                文件.write(文本内容)
            print(f"{日志前缀} 文件已保存至 {文件完整路径}")
            return (True,) 
        except Exception as e:
            print(f"{日志前缀} 保存文件时出错: {e}")
            return (False,)
