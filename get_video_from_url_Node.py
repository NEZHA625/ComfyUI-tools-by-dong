import os
import requests

class get_video_from_url_Node:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url": ("STRING", {"default": "https://api.kuleu.com/api/MP4_xiaojiejie?type=json"}),  
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")  
    RETURN_NAMES = ("success", "video_url")  
    FUNCTION = "fetch_video"  
    CATEGORY = "dong_tools/get_video_from_url_by_dong"

    def fetch_video(self,url,is_enable):

        if not is_enable:
            print("功能已禁用")
            return False, "功能已禁用"
            
        api_url = url

        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == 200 and "mp4_video" in data:
                return True, data["mp4_video"]
            else:
                return False, f"API返回异常: {data.get('msg', '未知错误')}"

        except requests.exceptions.RequestException as e:
            return False, f"请求错误: {str(e)}"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return True
