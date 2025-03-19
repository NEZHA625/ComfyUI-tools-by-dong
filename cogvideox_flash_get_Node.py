import os
import time
from check import check
from zhipuai import ZhipuAI
import yaml

class cogvideox_flash_get_Node:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "task_id": ("STRING",),
                "Retry_time": ("INT", {"default": 30}),
                "Retry_count": ("INT", {"default": 20}),
                "Delay_duration": ("INT", {"default": 60}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")  
    RETURN_NAMES = ("bool", "video_url") 
    FUNCTION = "cogvideox_flash_get" 
    CATEGORY = "dong_tools/cogvideox_flash_get_by_dong" 

    def cogvideox_flash_get(self, task_id, Retry_time, Retry_count, Delay_duration, is_enable):
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
        api_key = api_keys.get('zhipuqingyan', {}).get('api_key')

        if not api_key:
            print("API key 未设置")
            return False, None

        client = ZhipuAI(api_key=api_key)

        # 初次请求获取视频状态
        response = client.videos.retrieve_videos_result(id=task_id)
        
        def get_video_url():
            """从 response 获取视频 URL"""
            if response.task_status == "SUCCESS":
                if response.video_result and len(response.video_result) > 0:
                    return response.video_result[0].url
                else:
                    print("任务成功但未返回视频")
                    return None
            elif response.task_status == "FAILED":
                print("任务失败")
                return None
            return None  # 任务仍在处理中

        video_url = get_video_url()
        if video_url:
            return True, video_url

        # 任务仍在处理中，进入轮询等待
        time.sleep(Delay_duration)
        for i in range(Retry_count):
            response = client.videos.retrieve_videos_result(id=task_id)
            video_url = get_video_url()
            if video_url:
                return True, video_url
            
            print(f"视频仍在生成中，剩余重试次数: {Retry_count - i - 1}")
            time.sleep(Retry_time)

        print(f"所有重试失败，任务 ID: {task_id}")
        return False, "任务未能完成"

    @classmethod
    def IS_CHANGED(cls, video_url):
        return True
