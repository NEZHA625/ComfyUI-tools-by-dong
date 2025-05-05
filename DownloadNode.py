import os
import time
import subprocess
import re
from urllib.parse import urlparse
from check import check

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
ComfyUI_model_path = os.path.join(ComfyUI_path, "models")

comfyui_lora_path = os.path.join(ComfyUI_model_path, "loras")
comfyui_clip_path = os.path.join(ComfyUI_model_path, "clip")
comfyui_unet_path = os.path.join(ComfyUI_model_path, "unet")
comfyui_checkpoints_path = os.path.join(ComfyUI_model_path, "checkpoints")

class DownloadNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "url": ("STRING",),
                "type": (["lora", "clip", "unet", "checkpoints"], {"default": "lora"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "huggingface_accelerate": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")
    RETURN_NAMES = ("bool", "state")
    FUNCTION = "download"
    CATEGORY = "dong_tools/download_by_dong"

    def download(self, url, type, is_enable, huggingface_accelerate=False):
        if not check():
            print("未授权用户")
            return (False, "未授权")
        if not is_enable:
            return (False, "功能已禁用")
        if not url or "http" not in url:
            return (False, "无效的URL")
        
        # Handle huggingface mirror if needed
        if "huggingface.co" in url and huggingface_accelerate:
            a = "huggingface" + ".co"
            url = url.replace(a, "hf-mirror.com")
        
        # Determine download directory based on type
        if type == "lora":
            download_dir = comfyui_lora_path
        elif type == "clip":
            download_dir = comfyui_clip_path
        elif type == "unet":
            download_dir = comfyui_unet_path
        elif type == "checkpoints":
            download_dir = comfyui_checkpoints_path
        else:
            return (False, "无效的类型")
        
        # Create directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)
        
        try:
            # Parse filename from URL
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            
            # Check if file already exists
            file_path = os.path.join(download_dir, filename)
            if os.path.exists(file_path):
                return (True, f"文件已存在: {filename}")
            
            # Download using wget
            wget_command = [
                "wget",
                url,
                "-P", download_dir,
                "--no-check-certificate",
                "--content-disposition",
                "--progress=dot:giga"
            ]
            
            process = subprocess.Popen(
                wget_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Wait for download to complete
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.strip() if stderr else "未知错误"
                return (False, f"下载失败: {error_msg}")
            
            return (True, f"下载成功: {filename}")
            
        except Exception as e:
            return (False, f"下载出错: {str(e)}")

    @classmethod
    def IS_CHANGED(cls, is_enable):
        return True