import os
import shutil

class 移动文件节点:
    CATEGORY = "dong_tools/Move_File"
    RETURN_TYPES = ("BOOLEAN", "STRING")
    RETURN_NAMES = ("状态", "文件路径")
    FUNCTION = "move_file"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "源文件路径": ("STRING", {"default": ""}),
                "复制开关": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "目标文件夹路径": ("STRING", {"default": ""}),
                "自定义文件名": ("STRING", {"default": ""}),
            }
        }

    def move_file(self, 源文件路径, 复制开关=False, 目标文件夹路径="", 自定义文件名=""):
        try:
            # 检查源文件是否存在
            if not 源文件路径 or not os.path.isfile(源文件路径):
                return False, ""

            源文件路径 = os.path.abspath(源文件路径)
            源目录, 源文件名 = os.path.split(源文件路径)
            文件名, 扩展名 = os.path.splitext(源文件名)

            # 目标目录：未填写则使用源文件所在目录
            if 目标文件夹路径:
                目标文件夹路径 = os.path.abspath(目标文件夹路径)
            else:
                目标文件夹路径 = 源目录

            os.makedirs(目标文件夹路径, exist_ok=True)

            # 新文件名：未填写则保持原文件名
            if 自定义文件名:
                if os.path.splitext(自定义文件名)[1]:
                    最终文件名 = 自定义文件名
                else:
                    最终文件名 = 自定义文件名 + 扩展名
            else:
                最终文件名 = 源文件名

            目标文件路径 = os.path.join(目标文件夹路径, 最终文件名)

            # 执行复制或移动操作
            if 复制开关:
                shutil.copy2(源文件路径, 目标文件路径)
            else:
                shutil.move(源文件路径, 目标文件路径)

            return True, 目标文件路径

        except Exception:
            return False, ""