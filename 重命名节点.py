import os
import time

class 重命名节点:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "源文件路径": ("STRING", {"default": "source_directory"}), 
                "自定义文件名": ("STRING", {"default": "new_name"}),
                "节点开关": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")
    RETURN_NAMES = ("状态", "文件新路径")
    FUNCTION = "Rename"
    CATEGORY = "dong_tools/Rename_by_dong"  

    def Rename(self, 源文件路径, 自定义文件名, 节点开关):
        日志前缀 = "[重命名]"
        
        if not 节点开关:
            print(f"{日志前缀} 功能未启用")
            return (False, "") 

        if not os.path.exists(源文件路径):
            print(f"{日志前缀} 错误：文件 {源文件路径} 不存在")
            return (False, "文件不存在")

        # 获取文件的目录和扩展名
        文件目录 = os.path.dirname(源文件路径)
        文件扩展名 = os.path.splitext(源文件路径)[1]

        # 拼接新的文件路径
        新文件路径 = os.path.join(文件目录, 自定义文件名 + 文件扩展名)

        # 重命名文件
        try:
            os.rename(源文件路径, 新文件路径)
            print(f"{日志前缀} 文件已重命名为 {新文件路径}")
            return (True, 新文件路径)
        except Exception as e:
            print(f"{日志前缀} 重命名失败: {e}")
            return (False, "")
