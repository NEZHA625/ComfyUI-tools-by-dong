import os
import subprocess
import time
from check import check
class ZIPwith7zNode:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "source_file_path": ("STRING", {"default": "source_directory"}),  # 源路径
                "target_file_path": ("STRING", {"default": "target_directory"}),  # 目标路径
                "zip_name": ("STRING", {"default": "zip_name"}),  # 压缩包名称
                "is_delete_source": ("BOOLEAN", {"default": False}),  # 是否删除源文件
                "is_enable": ("BOOLEAN", {"default": False}),  # 功能开关
            }
        }

    RETURN_TYPES = ("BOOLEAN",)  # 返回类型是布尔值
    RETURN_NAMES = ("bool",)  # 返回变量名是bool
    FUNCTION = "ZIPwith7z"  # 执行的入口方法
    CATEGORY = "dong_tools/ZIP_by_dong"  # 分类，决定显示在哪一类节点下

    def ZIPwith7z(self, source_file_path, target_file_path, zip_name, is_delete_source, is_enable):
        time.sleep(3)  # 模拟延迟
        if not check():
            print("未授权用户")
            return (False,)
        if not is_enable:
            print("功能已禁用")
            return (False,)  # 如果禁用，则返回 False

        # 检查源文件夹路径是否存在
        if not os.path.exists(source_file_path):
            print(f"源文件路径不存在: {source_file_path}")
            return (False,)

        # 检查目标路径是否存在，不存在则创建
        if not os.path.exists(target_file_path):
            os.makedirs(target_file_path)
            print(f"目标文件夹创建成功: {target_file_path}")

        # 如果 zip_name 是路径，提取最后的文件夹名称作为压缩包名称
        if os.path.isdir(zip_name):
            zip_name = os.path.basename(os.path.normpath(zip_name))

        # 设置压缩包完整路径
        zip_file_path = os.path.join(target_file_path, f"{zip_name}.zip")

        # 使用7z命令进行压缩
        try:
            subprocess.run(
                ["7z", "a", "-tzip", zip_file_path, source_file_path],
                check=True
            )
            print(f"压缩完成: {zip_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"压缩失败: {e}")
            return (False,)

        # 如果is_delete_source为True，删除整个源文件夹
        if is_delete_source:
            try:
                if os.path.isdir(source_file_path):
                    import shutil
                    shutil.rmtree(source_file_path)  # 删除整个文件夹及其内容
                    print(f"源文件夹及其内容已删除: {source_file_path}")
                else:
                    os.remove(source_file_path)  # 如果是单个文件则删除文件
                    print(f"源文件删除成功: {source_file_path}")
            except Exception as e:
                print(f"删除源文件失败: {e}")
                return (False,)


        return (True,)

