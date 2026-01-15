import requests
from PIL import Image
import io
import numpy as np
import torch
from tqdm import tqdm
from typing import Union, List, Tuple, Optional
import tempfile
import os

def pil_to_tensor(
    pil_images: Union[Image.Image, List[Image.Image]],
    background_color: Union[Tuple[int, int, int], bool, None] = None,
    preserve_transparency: Optional[bool] = None,
) -> torch.Tensor:
    """
    将单个PIL图像或PIL图像列表转换为ComfyUI图像张量

    Args:
        pil_images: PIL图像或PIL图像列表
        background_color: 向后兼容参数 - 透明背景替换颜色，如果为tuple则不保留透明度
        preserve_transparency: 是否保留透明度信息，默认为True（除非指定了background_color）

    Returns:
        ComfyUI张量格式的图像
    """
    # 向后兼容性处理
    if background_color is not None and isinstance(background_color, tuple):
        # 旧API调用：指定了背景颜色，不保留透明度
        preserve_transparency = False
        bg_color = background_color
    else:
        # 新API调用：默认保留透明度
        if preserve_transparency is None:
            preserve_transparency = True
        bg_color = (0, 0, 0)  # 默认黑色背景
    if not isinstance(pil_images, list):
        pil_images = [pil_images]

    tensors = []
    for pil_image in pil_images:
        # 如果保留透明度且图像有alpha通道，则保持RGBA格式
        if preserve_transparency and pil_image.mode == "RGBA":
            # 保持RGBA格式
            processed_image = pil_image
        elif preserve_transparency and pil_image.mode in ("LA", "P"):
            # 将其他带透明度的格式转换为RGBA
            processed_image = pil_image.convert("RGBA")
        else:
            # 对于其他情况，转换为RGB（保持原有行为）
            if pil_image.mode == "RGBA":
                # processed_image = handle_transparent_background(pil_image, bg_color)
                pass
            elif pil_image.mode != "RGB":
                processed_image = pil_image.convert("RGB")
            else:
                processed_image = pil_image

        img_array = np.array(processed_image).astype(np.float32) / 255.0
        tensor = torch.from_numpy(img_array)[None,]
        tensors.append(tensor)

    if not tensors:
        # 如果列表为空，返回一个空的占位符张量
        channels = (
            4
            if (pil_images and pil_images[0].mode == "RGBA" and preserve_transparency)
            else 3
        )
        return torch.empty((0, 1, 1, channels), dtype=torch.float32)

    return torch.cat(tensors, dim=0)

def 下载图片(url, 保存路径=None, max_retry=5, timeout=600):
    """
    下载图片到本地并返回 PIL Image 或 tensor
    支持断点续传和重试
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    if 保存路径 is None:
        # 使用临时文件
        tmp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        保存路径 = tmp_file.name
        tmp_file.close()

    for attempt in range(max_retry):
        try:
            # 检查是否有未完成的文件
            resume_byte_pos = 0
            if os.path.exists(保存路径):
                resume_byte_pos = os.path.getsize(保存路径)

            # Range 支持断点续传
            headers_range = headers.copy()
            if resume_byte_pos > 0:
                headers_range['Range'] = f'bytes={resume_byte_pos}-'

            with requests.get(url, headers=headers_range, stream=True, timeout=timeout) as response:
                if response.status_code in (416, 404):
                    # 416 表示 Range 超出范围，重新下载
                    resume_byte_pos = 0
                    response = requests.get(url, headers=headers, stream=True, timeout=timeout)

                response.raise_for_status()

                total_size = int(response.headers.get('content-length', 0)) + resume_byte_pos
                block_size = 1024

                mode = 'ab' if resume_byte_pos > 0 else 'wb'
                with open(保存路径, mode) as f:
                    for data in tqdm(response.iter_content(block_size),
                                     initial=resume_byte_pos // block_size,
                                     total=max(total_size // block_size, 1),
                                     unit='KB', desc="下载进度"):
                        f.write(data)

            # 下载完成，打开 PIL
            img = Image.open(保存路径)
            tensor = pil_to_tensor(img)  # 调用你已有的 pil_to_tensor 函数
            return tensor

        except Exception as e:
            print(f"下载失败，第{attempt+1}次尝试: {e}")
            if attempt == max_retry - 1:
                print("下载最终失败")
                return None
            else:
                print("重试中...")

