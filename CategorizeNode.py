import os
import shutil
from check import check        
class CategorizeNode:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "prefix": ("STRING", {"default": "prefix"}),  # 前缀
                "source_file_path": ("STRING", {"default": "source_directory"}),
                "target_folder": ("STRING", {"default": "target_directory"}), 
                "is_enable": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)  # 返回类型是布尔值
    RETURN_NAMES = ("bool",)  # 返回变量名是bool
    FUNCTION = "Categorized_by_prefix"  # 执行的入口方法
    CATEGORY = "dong_tools/Categorized_by_dong"  # 分类，决定显示在哪一类节点下

    def Categorized_by_prefix(self, prefix, source_file_path, target_folder, is_enable):
        
        if not check():
            print("未授权用户")
            return (False,)
            
        if not is_enable:
            print("功能已禁用")
            return (False,)

        
        try:
            # 检查源路径是否存在
            if not os.path.exists(source_file_path):
                print(f"源文件路径不存在: {source_file_path}")
                return (False,)

            # 检查目标路径是否存在，如果不存在则创建
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            # 在目标路径下创建以 prefix 命名的子文件夹
            prefix_folder = os.path.join(target_folder, prefix)
            if not os.path.exists(prefix_folder):
                os.makedirs(prefix_folder)

            # 遍历源路径下的文件
            moved = False
            for filename in os.listdir(source_file_path):
                if filename.startswith(prefix) and filename != prefix:
                    source_file = os.path.join(source_file_path, filename)
                    shutil.move(source_file, prefix_folder)
                    print(f"move {source_file} -> {prefix_folder}")
                    moved = True

            if not moved:
                print(f"没有找到以 \"{prefix}\" 为前缀的文件")

            return (True,)

        except Exception as e:
            print(f"发生错误: {e}")
            return (False,)
