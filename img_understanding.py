import os
import time
from check import check
from zhipuai import ZhipuAI
import shutil
import requests
from huggingface_hub import HfApi
from urllib3.util.retry import Retry
import yaml
from requests.adapters import HTTPAdapter
from torchvision import transforms
import torch
import re
from PIL import Image, PngImagePlugin

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")

upload_path = os.path.join(ComfyUI_tools_by_dong_path, "img_understanding_tmp")

class img_understanding_Node:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Describe this image in detail."}), 
                "is_enable": ("BOOLEAN", {"default": True}),
                "domestic": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "image": ("IMAGE",),  
                "image_url":("STRING",),
            }
        }

    RETURN_TYPES = ("BOOLEAN","STRING")  
    RETURN_NAMES = ("bool","text") 
    FUNCTION = "img_understanding" 
    CATEGORY = "dong_tools/img_understanding_by_dong" 

    def img_understanding(self,prompt,is_enable,domestic,image=None,image_url=""):
        if not check():
            print("未授权用户")
            return (False,)
        
        if not is_enable:
            return "功能已禁用"
    
        if not os.path.exists(api_path):
            print("api_key未设置")
            return "api_key未设置，请使用set_api节点设置api"
    
        with open(api_path, 'r') as file:
            api_keys = yaml.safe_load(file)


        def img2url(image_):
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            else:
                shutil.rmtree(upload_path)
                os.makedirs(upload_path)
            img_path = os.path.join(upload_path, "understanding.png")
            try:
                img = image_
                image_single = img[0] 
                image_single = image_single.permute(2, 0, 1)
                to_pil = transforms.ToPILImage()
                img = to_pil(image_single)  
                if isinstance(img, Image.Image): 
                    img.save(img_path)
                    print(f"Image saved to {img_path}")
                else:
                    img = Image.open(img)
                    image_format = img.format
                    print(f"图像格式: {image_format}")
                    print("Provided image is not a valid PIL image.")
            except Exception as e:
                print(f"An error occurred while saving the image: {e}")
            else:
                print("Image is None, skipping.")

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

            model_repo = f"{username}/Img_for_understangding_temp"
    
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
                    # api.create_repo(model_repo, private=False, exist_ok=True)
                    api.upload_folder(folder_path=upload_path, repo_id=model_repo, repo_type="model")
                    print(f"Success_upload: {model_repo}")
                    url = f"{hf_endpoint}/{model_repo}/resolve/main/understanding.png?download=true"
                    return url
    
                except requests.exceptions.RequestException as e:
                    error_message = f"请求失败: {e}"
                    print(error_message)
                    if attempt < retries - 1:
                        print(f"等待 {2 ** attempt} 秒后重试...")
                        time.sleep(2 ** attempt)  # 指数退避策略
                    else:
                        return False
       
        api_key = api_keys['zhipuqingyan']['api_key']
        if image != None :
            IMG_URL = img2url(image)
        elif image_url != "":
            IMG_URL = image_url
        else:
            return (False,"Nothing detected")
     
        client = ZhipuAI(api_key=api_key)
        response = client.chat.completions.create(
            model="glm-4v-flash",
            messages=[
               {
                "role": "user",
                "content": [
                  {
                    "type": "text",
                    "text": prompt
                  },
                  {
                    "type": "image_url",
                    "image_url": {
                        "url" : IMG_URL
                    }
                  }
                ]
              }
            ]
        )
        respond_txt = response.choices[0].message.content
        return (True,respond_txt)

