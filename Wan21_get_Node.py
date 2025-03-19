import os
import time
from check import check
import json
import yaml
import requests
class Wan21_get_Node:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "task_id": ("STRING",),  
                "Retry_time": ("INT", {"default": 30}),
                "Retry_count": ("INT", {"default": 20}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN","STRING")  
    RETURN_NAMES = ("bool","image_url") 
    FUNCTION = "Wan21_get" 
    CATEGORY = "dong_tools/Wan21_by_dong" 

    def Wan21_get(self,task_id,Retry_time,Retry_count,is_enable):
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
    
        url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
        }
        
        payload = {
            "parameters": {
                "task_id":task_id,
            }
        }      
        
        response = requests.post(url, json=payload, headers=headers)
        
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
        
        if response_json['output']['task_status'] == "succeed":
            video_url = response_json['output']['video_url']
            return (True, video_url)

        for _ in range(Retry_count):  
            response_json = get_response_json()
            if response_json['output']['task_status'] == "SUCCEEDED":
                video_url = response_json['output']['video_url']
                return (True, video_url)
            elif response_json['output']['task_status'] == "FAILED":
                task_status_msg = response_json['output']['task_status']
                print (f"任务失败，失败原因为： {task_status_msg}")
                return (False, "任务失败，请检查终端")
            elif response_json['output']['task_status'] == "RUNNING":
                print (f"视频生成中，请耐心等待。--> task_id:{task_id}\n剩余重试次数: {Retry_count - _ - 1}")
                time.sleep(Retry_time) 
            elif response_json['output']['task_status'] == "PENDING":
                print(f"任务已提交，等待生成...--> task_id:{task_id}")
                time.sleep(Retry_time) 
            else:
                print(f"请求失败，正在重试... 剩余重试次数: {Retry_count - _ - 1}")
                time.sleep(Retry_time)
        
        print(f"所有重试都失败了 /(ㄒoㄒ)/~~ \n\n task_id = {task_id}")
        return (False, "请检查终端")

        

