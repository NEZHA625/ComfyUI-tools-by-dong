import os
import re
from check import check

class 路径加入节点:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "文件夹路径": ("STRING",),
                "自定义名称": ("STRING", {"default": "new_name"}),
                "新建文件夹": ("BOOLEAN", {"default": False}),
                "节点开关": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")
    RETURN_NAMES = ("bool", "file_path")
    FUNCTION = "路径加入"
    CATEGORY = "dong_tools/path_join_by_dong"

    def sanitize_file_name(self, file_name):
        return re.sub(r'[<>:"/\\|?*]', '_', file_name)

    def 路径加入(self, 文件夹路径, 自定义名称, 新建文件夹, 节点开关):
        # 授权检查
        if not check():
            print("未授权用户")
            return (False, "")

        # 节点开关
        if not 节点开关:
            print("功能已禁用")
            return (False, "")

        # 清理非法字符
        自定义名称 = self.sanitize_file_name(自定义名称)

        # 拼接路径
        file_path = os.path.join(文件夹路径, 自定义名称)

        # 不创建文件夹，只返回路径
        if not 新建文件夹:
            return (True, file_path)

        # 创建文件夹
        try:
            os.makedirs(file_path, exist_ok=True)
            return (True, file_path)
        except OSError as e:
            print(f"创建目录失败: {e}")
            return (False, "")

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return True
