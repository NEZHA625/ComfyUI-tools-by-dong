import os
import time
from PIL import Image
import imageio
from check import check
class Image2GIFNode:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "Images_path": ("STRING", {"default": "Images_path"}),  
                "is_enable": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("STRING", "BOOLEAN",)  # 返回类型
    RETURN_NAMES = ("gif_path", "bool",)  # 返回变量名
    FUNCTION = "Image2GIF"  # 执行的入口方法
    CATEGORY = "dong_tools/Image2GIF_by_dong"  # 分类，决定显示在哪一类节点下

    def Image2GIF(self, Images_path, is_enable):
        if not check():
            print("未授权用户")
            return (False,)
        if not is_enable:
            print("功能已禁用")
            return (False,)  # 如果禁用，返回 False

        # 检查文件夹是否存在以及文件夹里是否有图片
        if not os.path.exists(Images_path):
            print(f"错误：文件夹 {Images_path} 不存在")
            return (False,)

        # 获取文件夹里的所有图片文件
        image_files = [f for f in os.listdir(Images_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        if not image_files:
            print(f"错误：文件夹 {Images_path} 中没有图片")
            return (False,)

        # 按文件名排序，确保顺序
        image_files.sort()

        # 打开所有图片并存入列表
        images = []
        for image_file in image_files:
            image_path = os.path.join(Images_path, image_file)
            img = Image.open(image_path)
            images.append(img)

        # 创建 GIF 文件
        gif_path = os.path.join(Images_path, "output.gif")
        images[0].save(gif_path, save_all=True, append_images=images[1:], loop=0, duration=500,allow_unoptimized=True)  # duration 是每帧之间的延迟时间，单位为毫秒

        print(f"GIF 已生成：{gif_path}")
        return (gif_path,True)
