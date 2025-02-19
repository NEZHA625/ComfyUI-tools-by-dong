import os
import shutil
import time
class FileMoveNode:
    """
    文件移动节点

    Class methods
    -------------
    INPUT_TYPES (dict):
        定义节点输入参数的类型。
    FUNCTION (str):
        指定执行的入口方法。
    RETURN_TYPES (tuple):
        输出的类型。
    CATEGORY (str):
        分类。
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "filename_prefix": ("STRING", {"default": "file_prefix"}),  # 文件前缀
                "file_from_path": ("STRING", {"default": "source_directory"}),  # 源路径
                "file_to_path": ("STRING", {"default": "destination_directory"}),  # 目标路径
                "is_copy": ("BOOLEAN", {"default": True}),              
                "is_enable": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("BOOLEAN",)  # 返回类型是布尔值
    RETURN_NAMES = ("bool",)  # 返回变量名是bool
    FUNCTION = "move_files_by_prefix"  # 执行的入口方法
    CATEGORY = "dong_tools/move_files_by_dong"  # 分类，决定显示在哪一类节点下

    def move_files_by_prefix(self, filename_prefix, file_from_path, file_to_path,is_copy,is_enable):
        time.sleep(3)  # 模拟延迟
        if not is_enable:
            print("功能已禁用")
            return (False,)  # 如果禁用，则返回 False
        
        else:
            try:
                # 如果目标路径不存在，则创建该目录
                if not os.path.exists(file_to_path):
                    os.makedirs(file_to_path)

                # 获取源路径下所有文件
                files_to_move = [f for f in os.listdir(file_from_path) if f.startswith(filename_prefix)]

                # 如果没有找到符合条件的文件，则返回 False
                if not files_to_move:
                    print(f"没有找到符合前缀{filename_prefix}的文件。")
                    return (False,)

                # 移动符合条件的文件到目标路径
                for file_name in files_to_move:
                    source_file = os.path.join(file_from_path, file_name)
                    destination_file = os.path.join(file_to_path, file_name)
                    
                    if is_copy:
                        shutil.copy(source_file, destination_file)
                        print(f"文件 {file_name} 已成功复制到 {file_to_path}")   
                    else:
                        shutil.move(source_file, destination_file)
                        print(f"文件 {file_name} 已成功移动到 {file_to_path}")

                return (True,)  

            except Exception as e:
                error_message = f"文件移动/复制失败: {e}"
                print(error_message)
                return (False,)  # 如果出现错误，返回 False
