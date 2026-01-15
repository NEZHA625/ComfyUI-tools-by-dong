import os
import subprocess
import sys
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

class 模型下载节点:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "模型链接": ("STRING",),
                "模型类型": (["lora", "clip", "unet", "checkpoints"], {"default": "lora"}),
                "节点开关": ("BOOLEAN", {"default": True}),
                "HF加速": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")
    RETURN_NAMES = ("bool", "state")
    FUNCTION = "download"
    CATEGORY = "dong_tools/download_by_dong"

    def download(self, 模型链接, 模型类型, 节点开关, HF加速=False):
        if not check():
            print("未授权用户")
            return (False, "未授权")
        if not 节点开关:
            return (False, "功能已禁用")
        if not 模型链接 or "http" not in 模型链接:
            return (False, "无效的URL")
        
        # HuggingFace 镜像处理
        if "huggingface.co" in 模型链接 and HF加速:
            a = "huggingface" + ".co"
            模型链接 = 模型链接.replace(a, "hf-mirror.com")
        if 模型链接.endswith("?download=true"):
            模型链接 = 模型链接.replace("?download=true", "")
        
        # 下载目录
        if 模型类型 == "lora":
            下载目录 = comfyui_lora_path
        elif 模型类型 == "clip":
            下载目录 = comfyui_clip_path
        elif 模型类型 == "unet":
            下载目录 = comfyui_unet_path
        elif 模型类型 == "checkpoints":
            下载目录 = comfyui_checkpoints_path
        else:
            return (False, "无效的类型")
        os.makedirs(下载目录, exist_ok=True)

        try:
            文件名 = os.path.basename(urlparse(模型链接).path)
            文件路径 = os.path.join(下载目录, 文件名)
            if os.path.exists(文件路径):
                return (True, f"文件已存在: {文件名}")

            # 自动判断平台
            if sys.platform.startswith("win"):
                aria2c_path = os.path.join(ComfyUI_tools_by_dong_path, "aria2c.exe")
            else:
                aria2c_path = "aria2c"  # Linux / Mac 默认 PATH

            if not os.path.exists(aria2c_path) and sys.platform.startswith("win"):
                return (False, "未找到 aria2c.exe，请放在脚本目录下")

            # aria2c 下载命令
            aria2_command = [
                aria2c_path,
                "-x", "16",
                "-s", "16",
                "-d", 下载目录,
                "-o", 文件名,
                模型链接
            ]

            进程 = subprocess.Popen(
                aria2_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True
            )
            
            for line in 进程.stdout:
                print(line, end='')  # 保留进度条显示
            进程.wait()

            if 进程.returncode != 0:
                错误信息 = stderr.strip() if stderr else "未知错误"
                return (False, f"下载失败: {错误信息}")

            return (True, f"下载成功: {文件名}")

        except Exception as e:
            return (False, f"下载出错: {str(e)}")

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return True
