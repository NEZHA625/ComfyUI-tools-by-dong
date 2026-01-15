import os
import time
import subprocess
import re
from urllib.parse import urlparse
from check import check

class 文件下载节点:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "下载链接": ("STRING",),
                "文件类型": (["auto", "mp4", "avi", "png", "jpg", "jpeg", "gif", "pdf", "docx", "txt", "xlsx", "pptx", "pth", "safetensors"], {"default": "auto"}),
                "节点开关": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "自定义文件名": ("STRING",),
                "保存文件夹路径": ("STRING",),
                "HF加速开关": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")
    RETURN_NAMES = ("状态", "文件路径")
    FUNCTION = "download_from_url"  # 函数入口
    CATEGORY = "dong_tools/download_anyting_by_dong"

    @staticmethod
    def 获取文件扩展名(链接):
        """解析 URL 获取文件扩展名"""
        parsed_url = urlparse(链接)
        路径 = parsed_url.path
        文件名 = os.path.basename(路径)

        match = re.search(r'\.([a-zA-Z0-9]+)$', 文件名)
        if match:
            return match.group(1)  # 返回文件扩展名，不带点
        return None  # 如果没有找到扩展名，返回 None

    def download_from_url(
        self,
        下载链接,
        文件类型,
        节点开关,
        自定义文件名,
        保存文件夹路径="",
        HF加速开关=True
    ):
        """从 URL 下载文件"""
        if not check():
            print("未授权用户")
            return (False, "未授权")

        if not 节点开关:
            return (False, "功能已禁用")

        if not 下载链接 or "http" not in 下载链接:
            return (False, "无效的URL")
            
        if "huggingface.co" in 下载链接 and HF加速开关:
            a = "huggingface" + ".co"
            下载链接 = 下载链接.replace(a, "hf-mirror.com")

        # 如果文件类型为 auto，自动从 URL 中获取扩展名
        if 文件类型 == "auto":
            文件类型 = self.获取文件扩展名(下载链接) or "temp"

        try:
            # 确定文件存储路径
            当前目录 = os.path.dirname(os.path.abspath(__file__))
            默认下载目录 = os.path.join(当前目录, 'download_temp')
            if 保存文件夹路径 != "":
                默认下载目录 = 保存文件夹路径
            os.makedirs(默认下载目录, exist_ok=True)
            时间戳 = int(time.time())

            # 如果没有提供文件名，使用时间戳作为文件名
            if not 自定义文件名:
                文件路径 = os.path.join(默认下载目录, f'download-{时间戳}.{文件类型}')
            else:
                文件路径 = os.path.join(默认下载目录, f'{自定义文件名}-{时间戳}.{文件类型}')

            # 使用 aria2c 下载文件
            cmd = [
                "aria2c", "-o", os.path.basename(文件路径), "-x", "16", "-s", "16", 下载链接, "-d", 默认下载目录
            ]
            subprocess.run(cmd, check=True)  # 执行下载命令
            return (True, 文件路径)

        except subprocess.CalledProcessError as e:
            return (False, f"下载失败: {str(e)}")

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return True
