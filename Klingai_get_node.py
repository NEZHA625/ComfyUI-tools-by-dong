import os
import requests
import json
import time
from check import check
import jwt
import yaml
import re

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")

class Get_video_Node:
        
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "task_id": ("STRING",), 
                "task_type": ("STRING",),  
                "is_enable": ("BOOLEAN", {"default": True}),
                "Retry_time": ("INT", {"default": 30}),
                "Retry_count": ("INT", {"default": 20}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")  
    RETURN_NAMES = ("bool", "video_url") 
    FUNCTION = "get_video" 
    CATEGORY = "dong_tools/get_video_by_dong" 

    def get_video(self, task_id, task_type, is_enable, Retry_time, Retry_count):
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
        
        url = f"https://api.klingai.com/v1/videos/{task_type}/{task_id}"

        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }

        def get_response_json():    
            try:
                response_data = requests.get(url, headers=headers)
                response_data.raise_for_status() 
                response_json = response_data.json()
                return response_json
            except requests.exceptions.RequestException as e:
                print(f"请求失败: {e}")
                return None 
                
        response_json = get_response_json()
        print(response_json)
        
        if response_json['data']['task_status'] == "succeed":
            video_url = response_json['data']['task_result']['videos'][0]['url']
            return (True, video_url)
        
        for _ in range(Retry_count):  # 重试控制
            response_json = get_response_json()
            if response_json['data']['task_status'] == "succeed":
                video_url = response_json['data']['task_result']['videos'][0]['url']
                return (True, video_url)
            elif response_json['data']['task_status'] == "failed":
                task_status_msg = response_json['data']['task_status_msg']
                print (f"任务失败，失败原因为： {task_status_msg}")
                return (False, "任务失败，请检查终端")
            elif response_json['data']['task_status'] == "processing":
                print (f"视频生成中，请耐心等待。--> task_id:{task_id}\n剩余重试次数: {Retry_count - _ - 1}")
                time.sleep(Retry_time) 
            elif response_json['data']['task_status'] == "submitted":
                print(f"任务已提交，等待生成...--> task_id:{task_id}")
                time.sleep(Retry_time) 
            else:
                print(f"请求失败，正在重试... 剩余重试次数: {Retry_count - _ - 1}")
                time.sleep(Retry_time)
        
        print(f"所有重试都失败了 /(ㄒoㄒ)/~~ \n\n task_id = {task_id}")
        return (False, "请检查终端")

