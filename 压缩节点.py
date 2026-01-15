import os
import subprocess
import shutil
from check import check

class 压缩节点:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "源文件路径": ("STRING",), 
                "目标文件夹路径": ("STRING",),
                "压缩包名称": ("STRING",), 
                "压缩后删除源文件": ("BOOLEAN", {"default": False}),
                "节点开关": ("BOOLEAN", {"default": False}),  
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING",)
    RETURN_NAMES = ("状态", "压缩包路径",)
    FUNCTION = "ZIPwith7z"
    CATEGORY = "dong_tools/ZIP_by_dong"

    def ZIPwith7z(self, 源文件路径, 目标文件夹路径, 压缩包名称, 压缩后删除源文件, 节点开关):
        日志前缀 = "[ZIPwith7z]"

        if not 节点开关:
            print(f"{日志前缀} 功能未启用")
            return (False, "")

        # 源路径检查
        if not os.path.exists(源文件路径):
            print(f"{日志前缀} 源文件路径不存在: {源文件路径}")
            return (False, "")
            
        # 如果目标路径为空，则使用源文件所在目录
        if not 目标文件夹路径 or 目标文件夹路径.strip() == "":
            目标文件夹路径 = os.path.dirname(os.path.abspath(源文件路径))
            
        # 创建目标文件夹（如果不存在）
        try:
            os.makedirs(目标文件夹路径, exist_ok=True)
        except Exception as e:
            print(f"{日志前缀} 创建目标文件夹失败: {e}")
            return (False, "")

        # 压缩包名称处理
        if not 压缩包名称 or 压缩包名称.strip() == "":
            压缩包名称 = os.path.basename(os.path.normpath(源文件路径)) or "archive"

        压缩包路径 = os.path.abspath(os.path.join(目标文件夹路径, f"{压缩包名称}.zip"))

        # 判断是否需要排除压缩包自身
        排除参数 = []
        if os.path.abspath(源文件路径) == os.path.abspath(目标文件夹路径):
            排除参数 = [f"-x!{os.path.basename(压缩包路径)}"]

        # 调用 7z 压缩（实时打印输出 + 排除 zip 文件自身）
        try:
            进程 = subprocess.Popen(
                ["7z", "a", "-tzip", 压缩包路径, 源文件路径] + 排除参数,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            # 实时读取 7z 输出并打印
            for 行 in 进程.stdout:
                if 行.strip():
                    print(f"{日志前缀} {行.strip()}")

            进程.wait()
            if 进程.returncode != 0:
                print(f"{日志前缀} 压缩失败，错误码: {进程.returncode}")
                return (False, "")

            print(f"{日志前缀} 压缩完成: {压缩包路径}")

        except FileNotFoundError:
            print(f"{日志前缀} 未找到 7z 命令，请确认已安装并加入系统 PATH")
            return (False, "")
        except Exception as e:
            print(f"{日志前缀} 压缩过程异常: {e}")
            return (False, "")

        # 删除源文件/目录（保留压缩包）
        if 压缩后删除源文件:
            try:
                if os.path.isdir(源文件路径):
                    for 项目 in os.listdir(源文件路径):
                        项目路径 = os.path.join(源文件路径, 项目)
                        # 跳过压缩包本身
                        if os.path.abspath(项目路径) == os.path.abspath(压缩包路径):
                            continue
                        if os.path.isdir(项目路径):
                            shutil.rmtree(项目路径)
                        else:
                            os.remove(项目路径)
                    print(f"{日志前缀} 源目录内容已删除（保留压缩包）: {源文件路径}")
                else:
                    if os.path.abspath(源文件路径) != os.path.abspath(压缩包路径):
                        os.remove(源文件路径)
                        print(f"{日志前缀} 源文件删除成功: {源文件路径}")
            except Exception as e:
                print(f"{日志前缀} 删除源文件失败: {e}")
                return (False, "")

        return (True, 压缩包路径)
