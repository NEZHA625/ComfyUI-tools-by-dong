import os
import shutil
import requests
from urllib3.util.retry import Retry
import yaml
from requests.adapters import HTTPAdapter
from check import check
from torchvision import transforms
import torch
import re
from PIL import Image, PngImagePlugin
from pathlib import Path
from datetime import datetime, timedelta

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)

api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")
upload_path = os.path.join(ComfyUI_tools_by_dong_path, "img2url_tmp")

class img2url_v2_Node:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "model_name": ("STRING",{"default": "qwen-vl-plus"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN","STRING")
    RETURN_NAMES = ("bool","url")
    FUNCTION = "img2url_v2"
    CATEGORY = "ABC/img2url_v2_by_dong"

    def img2url_v2(self, image, model_name, is_enable):
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

        img_path = os.path.join(upload_path, "image.png")
        image_single = image[0] 
        image_single = image_single.permute(2, 0, 1) 
        to_pil = transforms.ToPILImage()
        img = to_pil(image_single)  
        img.save(img_path)
        
        if not os.path.exists(api_path):
            print("api_key未设置，请使用set_api节点设置api")
            return (False,)
        else:
            with open(api_path, 'r') as file:
                api_keys = yaml.safe_load(file)
            api_key = api_keys['aliyun_bailian']['api_key']

        def get_upload_policy(api_key, model_name):
            url = "https://dashscope.aliyuncs.com/api/v1/uploads"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            params = {
                "action": "getPolicy",
                "model": model_name
            }
            
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                raise Exception(f"Failed to get upload policy: {response.text}")
            
            return response.json()['data']
        
        def upload_file_to_oss(policy_data, file_path):
            file_name = Path(file_path).name
            key = f"{policy_data['upload_dir']}/{file_name}"
            with open(file_path, 'rb') as file:
                files = {
                    'OSSAccessKeyId': (None, policy_data['oss_access_key_id']),
                    'Signature': (None, policy_data['signature']),
                    'policy': (None, policy_data['policy']),
                    'x-oss-object-acl': (None, policy_data['x_oss_object_acl']),
                    'x-oss-forbid-overwrite': (None, policy_data['x_oss_forbid_overwrite']),
                    'key': (None, key),
                    'success_action_status': (None, '200'),
                    'file': (file_name, file)
                }
                response = requests.post(policy_data['upload_host'], files=files)
                if response.status_code != 200:
                    raise Exception(f"Failed to upload file: {response.text}")
            return f"oss://{key}"
        
        def upload_file_and_get_url(api_key, model_name, file_path):
            policy_data = get_upload_policy(api_key, model_name) 
            oss_url = upload_file_to_oss(policy_data, file_path)
            return oss_url
    
        model_name = model_name
        file_path = img_path  
        try:
            public_url = upload_file_and_get_url(api_key, model_name, file_path)
            expire_time = datetime.now() + timedelta(hours=48)
            print(f"文件上传成功，有效期为48小时，过期时间: {expire_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"公网URL: {public_url}")
            return(True,public_url)
    
        except Exception as e:
            print(f"Error: {str(e)}")
            return(False,)


