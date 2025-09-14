import os
import subprocess
import shutil
from check import check

class ZIPwith7zNode:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """返回节点输入参数配置"""
        return {
            "required": {
                "source_file_path": ("STRING",),  # 源路径
                "target_file_path": ("STRING",),  # 目标路径
                "zip_name": ("STRING",),  # 压缩包名称
                "is_delete_source": ("BOOLEAN", {"default": False}),  # 是否删除源文件
                "is_enable": ("BOOLEAN", {"default": False}),  # 功能开关
            }
        }

    # 增加返回压缩包路径
    RETURN_TYPES = ("BOOLEAN", "STRING",)
    RETURN_NAMES = ("bool", "zip_file_path",)
    FUNCTION = "ZIPwith7z"
    CATEGORY = "dong_tools/ZIP_by_dong"

    def ZIPwith7z(self, source_file_path, target_file_path, zip_name, is_delete_source, is_enable):
        log_prefix = "[ZIPwith7z]"

        # 授权检查
        if not check():
            print(f"{log_prefix} 未授权用户")
            return (False, "")

        if not is_enable:
            print(f"{log_prefix} 功能已禁用")
            return (False, "")

        # 源路径检查
        if not os.path.exists(source_file_path):
            print(f"{log_prefix} 源文件路径不存在: {source_file_path}")
            return (False, "")
            
        if not target_file_path or target_file_path.strip() == "":
            target_file_path = source_file_path
            
        # 目标路径检查/创建
        try:
            os.makedirs(target_file_path, exist_ok=True)
        except Exception as e:
            print(f"{log_prefix} 创建目标文件夹失败: {e}")
            return (False, "")

        # 压缩包名称处理
        if not zip_name or zip_name.strip() == "":
            zip_name = os.path.basename(os.path.normpath(source_file_path)) or "archive"

        zip_file_path = os.path.abspath(os.path.join(target_file_path, f"{zip_name}.zip"))

        # 判断是否需要排除压缩包自身
        exclude_arg = []
        if os.path.abspath(source_file_path) == os.path.abspath(target_file_path):
            exclude_arg = [f"-x!{os.path.basename(zip_file_path)}"]

        # 调用 7z 压缩（实时打印输出 + 排除 zip 文件自身）
        try:
            process = subprocess.Popen(
                ["7z", "a", "-tzip", zip_file_path, source_file_path] + exclude_arg,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            # 实时读取 7z 输出并打印
            for line in process.stdout:
                if line.strip():
                    print(f"{log_prefix} {line.strip()}")

            process.wait()
            if process.returncode != 0:
                print(f"{log_prefix} 压缩失败，错误码: {process.returncode}")
                return (False, "")

            print(f"{log_prefix} 压缩完成: {zip_file_path}")

        except FileNotFoundError:
            print(f"{log_prefix} 未找到 7z 命令，请确认已安装并加入系统 PATH")
            return (False, "")
        except Exception as e:
            print(f"{log_prefix} 压缩过程异常: {e}")
            return (False, "")

        # 删除源文件/文件夹（保留压缩包）
        if is_delete_source:
            try:
                if os.path.isdir(source_file_path):
                    for item in os.listdir(source_file_path):
                        item_path = os.path.join(source_file_path, item)
                        # 跳过压缩包本身
                        if os.path.abspath(item_path) == os.path.abspath(zip_file_path):
                            continue
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)
                    print(f"{log_prefix} 源目录内容已删除（保留压缩包）: {source_file_path}")
                else:
                    if os.path.abspath(source_file_path) != os.path.abspath(zip_file_path):
                        os.remove(source_file_path)
                        print(f"{log_prefix} 源文件删除成功: {source_file_path}")
            except Exception as e:
                print(f"{log_prefix} 删除源文件失败: {e}")
                return (False, "")

        return (True, zip_file_path)
