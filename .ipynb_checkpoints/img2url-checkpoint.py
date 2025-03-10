import os
import shutil
import requests
from huggingface_hub import HfApi
from urllib3.util.retry import Retry
import yaml
import time
from requests.adapters import HTTPAdapter
from check import check
from torchvision import transforms
import torch
import re
from PIL import Image, PngImagePlugin
import base64

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)

api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")
upload_path = os.path.join(ComfyUI_tools_by_dong_path, "img2url_tmp")

class IMG2URLNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image1": ("IMAGE",),
                "domestic": ("BOOLEAN", {"default": True}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "only_base": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "image2":("IMAGE",),
                "image3":("IMAGE",),
                "image4":("IMAGE",),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "BOOLEAN","STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("url1", "url2", "url3", "url4", "bool","base1","base2","base3","base4",)
    FUNCTION = "img2url"
    CATEGORY = "dong_tools/img2url_by_dong"

    def img2url(self, image1, domestic, is_enable, only_base, image2=None, image3=None, image4=None):
            
        def image_to_base64(image_path):
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
        
        if not check():
            print("未授权用户")
            return (False,)
    
        if not is_enable:
            print("功能已禁用")
            return (False,)
            
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        else:
            shutil.rmtree(upload_path)
            os.makedirs(upload_path)
        
        image_list = [image1, image2, image3, image4]
        saved_images = 0
        base_list = []  # 用来存放 Base64 编码
        for i, img in enumerate(image_list, 1):
            if img is not None:
                img_path = os.path.join(upload_path, f"image{i}.png")
                try:
                    image_single = img[0]  # 选择第一张图像，形状为 (H, W, C)
                    image_single = image_single.permute(2, 0, 1)  # 转换为 (C, H, W)
                    to_pil = transforms.ToPILImage()
                    img = to_pil(image_single)  
                    if isinstance(img, Image.Image): 
                        img.save(img_path)
                        base = image_to_base64(img_path)  # 获取 Base64 编码
                        base_list.append(base)  # 保存到 Base64 编码列表
                        print(f"Image saved to {img_path}")
                        saved_images += 1
                    else:
                        img = Image.open(img)
                        image_format = img.format
                        print(f"图像格式: {image_format}")
                        print("Provided image is not a valid PIL image.")
                except Exception as e:
                    print(f"An error occurred while saving the image: {e}")
            else:
                print(f"Image {i} is None, skipping.")
        
        if saved_images == 0:
            print("There are no images")
            return (False,)
            
        if only_base :
            return ("only_base_mode","only_base_mode","only_base_mode", "only_base_mode", False,
                    base_list[0] if len(base_list) > 0 else None,
                    base_list[1] if len(base_list) > 1 else None,
                    base_list[2] if len(base_list) > 2 else None,
                    base_list[3] if len(base_list) > 3 else None)
        if not os.path.exists(api_path):
            print("api_key未设置，请使用set_api节点设置api")
            return (False,)
        else:
            with open(api_path, 'r') as file:
                api_keys = yaml.safe_load(file)
            username = api_keys['huggingface']['hf_name']
            user_token = api_keys['huggingface']['hf_key']
            
        hf_endpoint = "https://huggingface"+".co" if not domestic else "https://hf-mirror.com"
        api = HfApi(endpoint=hf_endpoint, token=user_token)
    
        model_id = "Imgbed"
        model_repo = f"{username}/{model_id}"
    
        try:
            api.repo_info(model_repo)
            print(f"Repo {model_repo} 已存在")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"{model_repo} 不存在，正在创建...")
                api.create_repo(model_repo, private=False, exist_ok=True)
            elif e.response.status_code == 403:
                error_message = f"访问被拒绝：你没有权限访问仓库 {model_repo}。"
                print(error_message)
            else:
                raise e
    
        print(f"start upload images: {model_repo}...")
    
        retries = 3
            
        for attempt in range(retries):
            try:
                api.upload_folder(folder_path=upload_path, repo_id=model_repo, repo_type="model")
                print(f"Success_upload: {model_repo}")
                url1 = f"{hf_endpoint}/{model_repo}/resolve/main/image1.png?download=true" if len(base_list) > 0 else None
                url2 = f"{hf_endpoint}/{model_repo}/resolve/main/image2.png?download=true" if len(base_list) > 1 else None
                url3 = f"{hf_endpoint}/{model_repo}/resolve/main/image3.png?download=true" if len(base_list) > 2 else None
                url4 = f"{hf_endpoint}/{model_repo}/resolve/main/image4.png?download=true" if len(base_list) > 3 else None
    
                return (url1, url2, url3, url4, True,
                        base_list[0] if len(base_list) > 0 else None,
                        base_list[1] if len(base_list) > 1 else None,
                        base_list[2] if len(base_list) > 2 else None,
                        base_list[3] if len(base_list) > 3 else None)
    
            except requests.exceptions.RequestException as e:
                error_message = f"请求失败: {e}"
                print(error_message)
                if attempt < retries - 1:
                    print(f"等待 {2 ** attempt} 秒后重试...")
                    time.sleep(2 ** attempt)  # 指数退避策略
                else:
                    return (error_message, error_message, error_message, error_message, False,
                            base_list[0] if len(base_list) > 0 else None,
                            base_list[1] if len(base_list) > 1 else None,
                            base_list[2] if len(base_list) > 2 else None,
                            base_list[3] if len(base_list) > 3 else None)
