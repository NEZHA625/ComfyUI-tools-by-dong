import os
import time
class RenameNode:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "file_absolute_path": ("STRING", {"default": "source_directory"}),  # 源路径
                "file_new_name": ("STRING", {"default": "new_name"}),  # 目标文件名
                "is_enable": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)  # 返回类型是布尔值
    RETURN_NAMES = ("bool",)  # 返回变量名是bool
    FUNCTION = "Rename"  # 执行的入口方法
    CATEGORY = "dong_tools/Rename_by_dong"  # 分类，决定显示在哪一类节点下

    def Rename(self, file_absolute_path, file_new_name, is_enable):
        
        time.sleep(3)  # 模拟延迟
        
        if not is_enable:
            print("功能已禁用")
            return (False,)  # 如果禁用，则返回 False

        # 检查文件是否存在
        if not os.path.exists(file_absolute_path):
            print(f"错误：文件 {file_absolute_path} 不存在")
            return (False,)

        # 获取文件的目录和扩展名
        file_dir = os.path.dirname(file_absolute_path)
        file_ext = os.path.splitext(file_absolute_path)[1]

        # 拼接新的文件路径
        new_file_path = os.path.join(file_dir, file_new_name + file_ext)

        # 重命名文件
        try:
            os.rename(file_absolute_path, new_file_path)
            print(f"文件已重命名为 {new_file_path}")
            return (True,)
        except Exception as e:
            print(f"重命名失败: {e}")
            return (False,)

    @classmethod
    def IS_CHANGED(cls, file_absolute_path, file_new_name, is_enable):
        return True
