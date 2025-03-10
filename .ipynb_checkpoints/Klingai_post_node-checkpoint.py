import os
import requests
import json
from check import check
import jwt
import yaml
import time
import re

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")

class klingai_video_Node:
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "model": (["v1","v1.6"], {"default": "v1"}), 
                "prompt": ("STRING",),  
                "negative_prompt": ("STRING",),  
                "cfg_scale": ([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],{"default": 0.5}),  
                "mode": (["std","pro"] ,{"default": "std"}),  
                "aspect_ratio": (["16:9","9:16","1:1"], {"default": "9:16"}),  
                "video_time": (["5s","10s"], {"default": "5s"}), 
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional":{
            "image_url":("STRING",), 
            "image_tail_url":("STRING",), 
            }
        }

    RETURN_TYPES = ("BOOLEAN","STRING","STRING")  
    RETURN_NAMES = ("bool","task_id","task_type") 
    FUNCTION = "video" 
    CATEGORY = "dong_tools/video_by_dong" 

    def video(self,model,prompt,negative_prompt,cfg_scale,mode,aspect_ratio, video_time,is_enable,image_url=None,image_tail_url=None):
        def encode_jwt_token():
            if not os.path.exists(api_path):
                return ("NONE")
                print("api_key未设置")
                
            with open(api_path, 'r') as file:
                api_keys = yaml.safe_load(file)
        
            ak = api_keys['Klingai']['AccessKey_ID']
            sk = api_keys['Klingai']['AccessKey_Secret']
                
            headers = {
                "alg": "HS256",
                "typ": "JWT"
            }
            payload = {
                "iss": ak,
                "exp": int(time.time()) + 7200,
                "nbf": int(time.time()) - 5 
            }
            token = jwt.encode(payload, sk, headers=headers)
            return token
            
        token = encode_jwt_token()
        
        if not check():
            print("未授权用户")
            return (False,)
            
        if not is_enable:
            print("功能已禁用")
            return (False,) 
        
        model_name = "kling-v1" if model == "v1" else "kling-v1-6"
        
        duration = "5" if video_time == "5s" else "10"
        
        task = "text2video" if image_url == None else "image2video"
        
        print(f"selected task: {task}")
            
        url = f"https://api.klingai.com/v1/videos/{task}"

        common_headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
        
        common_payload = {
            "model_name": model_name,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "mode": mode,
            "cfg_scale": cfg_scale,
            "duration": duration
        }
        
        if task == "text2video":
            payload = common_payload.copy() 
            payload.update({"aspect_ratio": aspect_ratio}) 
        
        elif image_tail_url !=None :
            payload = common_payload.copy()  
            payload.update({"image": image_url}) 
            payload.update({"image_tail": image_tail_url})
        else:
            payload = common_payload.copy()  
            payload.update({"image": image_url}) 
        
        headers = common_headers
                
        try:
            response_data = requests.post(url, json=payload, headers=headers)
            response_data.raise_for_status()  
            response_json = response_data.json()
          
            print(response_json)
            task_id = response_json['data']['task_id']
            return (True,task_id,task)

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return (False,"请检查终端")
        

