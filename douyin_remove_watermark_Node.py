import os
import requests
from check import check
import re

class douyin_remove_watermark_Node:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "douyin_url": ("STRING",),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")
    RETURN_NAMES = ("bool", "video_url")
    FUNCTION = "douyin"
    CATEGORY = "dong_tools/douyin_remove_watermark_by_dong"

    def douyin(self, douyin_url):
        
        if not check():
            print("未授权用户")
            return False, "未授权用户"
            
        def extract_douyin_url(text):
            pattern = r"https://v\.douyin\.com/\S+/"
            match = re.search(pattern, text)
            return match.group(0) if match else None
    
        douyin_url = extract_douyin_url(douyin_url)
        
        print(douyin_url)
        
        api_url=f"https://api.xinyew.cn/api/douyinjx?url={douyin_url}"
        
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return (True,data.get("data", {}).get("video_url", "未找到视频链接"))
            
            # if data.get("code") == 200 and "video_url" in data.get("data", {}):
            #     return True, data["video_url"]
            # else:
            #     return False, f"API返回异常: {data.get('msg', '未知错误')}"
    
        except requests.exceptions.RequestException as e:
            return f"请求错误: {str(e)}"
