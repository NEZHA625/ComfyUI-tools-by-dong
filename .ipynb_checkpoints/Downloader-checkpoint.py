import os
import time
import subprocess
import re
from urllib.parse import urlparse
from check import check

class Downloader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "url": ("STRING",),
                "file_type": (["auto", "mp4", "avi", "png", "jpg", "jpeg", "gif", "pdf", "docx", "txt", "xlsx", "pptx", "pth", "safetensors"], {"default": "auto"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "file_name": ("STRING",),
                "download_folder": ("STRING",),
                "huggingface_accelerate": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")
    RETURN_NAMES = ("bool", "path")
    FUNCTION = "download_from_url"  # 函数入口
    CATEGORY = "dong_tools/download_anyting_by_dong"

    @staticmethod
    def get_file_extension(url):
        """解析 URL 获取文件扩展名"""
        parsed_url = urlparse(url)
        path = parsed_url.path
        file_name = os.path.basename(path)

        match = re.search(r'\.([a-zA-Z0-9]+)$', file_name)
        if match:
            return match.group(1)  # 返回文件扩展名，不带点
        return None  # 如果没有找到扩展名，返回 None

    def download_from_url(self, url, file_type, is_enable, file_name,download_folder="",huggingface_accelerate=True):
        """从 URL 下载文件"""
        if not check():
            print("未授权用户")
            return (False, "未授权")

        if not is_enable:
            return (False, "功能已禁用")

        if not url or "http" not in url:
            return (False, "无效的URL")
            
        if "huggingface.co" in url and huggingface_accelerate:
            a = "huggingface" + ".co"
            url = url.replace(a, "hf-mirror.com")


        # 如果文件类型为 auto，自动从 URL 中获取扩展名
        if file_type == "auto":
            file_type = self.get_file_extension(url) or "temp"

        try:
            # 确定文件存储路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            download_temp_dir = os.path.join(current_dir, 'download_temp')
            if download_folder != "":
                download_temp_dir = download_folder
            os.makedirs(download_temp_dir, exist_ok=True)
            timestamp = int(time.time())

            # 如果没有提供文件名，使用时间戳作为文件名
            if not file_name:
                file_path = os.path.join(download_temp_dir, f'download-{timestamp}.{file_type}')
            else:
                file_path = os.path.join(download_temp_dir, f'{file_name}-{timestamp}.{file_type}')

            # 使用 aria2c 下载文件
            cmd = [
                "aria2c", "-o", os.path.basename(file_path), "-x", "16", "-s", "16", url, "-d", download_temp_dir
            ]
            subprocess.run(cmd, check=True)  # 执行下载命令
            return (True, file_path)

        except subprocess.CalledProcessError as e:
            return (False, f"下载失败: {str(e)}")

    @classmethod
    def IS_CHANGED(cls, is_enable):
        """检查功能是否已变更"""
        return True
