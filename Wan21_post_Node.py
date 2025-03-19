import os
import time
from check import check
import json
import yaml
import random
import requests
class Wan21_post_Node:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": (["wanx2.1-t2v-turbo","wanx2.1-t2v-plus", "wanx2.1-i2v-turbo","wanx2.1-i2v-plus"],{"default": "wanx2.1-t2v-turbo"}), 
                "prompt": ("STRING",),  
                "prompt_extend": ("BOOLEAN", {"default": False}),
                "size":(["720*1280","832*1088", "960*960","1088*832","1280*720"],{"default": "720*1280"}),
                "duration":("INT",{"default": "5"}),
                "seed":("INT",{"default": "-1"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional":{
                "image_url": ("STRING",),  
            }
        }

    RETURN_TYPES = ("BOOLEAN","STRING")  
    RETURN_NAMES = ("bool","task_id") 
    FUNCTION = "Wan21_post" 
    CATEGORY = "dong_tools/Wan21_post_by_dong" 

    def Wan21_post(self,model,prompt,prompt_extend,size,duration,seed,is_enable,image_url):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        api_path = os.path.join(os.path.dirname(os.path.dirname(script_dir)), "api_by_dong.yaml")
        
        if not is_enable:
            print("功能已禁用")
            return False, None

        if not check():
            print("未授权用户")
            return False, None

        if not os.path.exists(api_path):
            print("API key 文件未找到")
            return False, None
            
        with open(api_path, 'r') as file:
            api_keys = yaml.safe_load(file)
        api_key = api_keys.get('aliyun_bailian', {}).get('api_key')

        if not api_key:
            print("API key 未设置")
            return False, None

        if seed == "-1":
            seed = random[0, 2147483647]
        elif 0<seed<2147483647:
            pass
        else:
            return (False,"seed out of range")
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis"
        
        headers = {
            "X-DashScope-Async": "enable",
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        if "t2v" not in model: 
            payload = {
                "model": model,
                "input": {
                    "prompt": prompt,
                    "img_url": image_url
                },
                "parameters": {
                    "duration":duration,
                    "seed":seed,
                    "prompt_extend":prompt_extend 
                }
            }
        else:
            payload = {
                "model": model,
                "input": {
                    "prompt": prompt
                },
                "parameters": {
                    "size": size,
                    "duration":duration,
                    "seed":seed,
                    "prompt_extend":prompt_extend 
                }
            }            
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            response_data = response.json()
            task_id = response_data["output"].get("task_id")
            return (True, task_id if task_id else None)
        else:
            return (False, "error")

        

