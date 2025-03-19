import os
import time
from check import check
from zhipuai import ZhipuAI
import yaml

class cogvideox_flash_post_Node:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING",),  
                "with_audio": ("BOOLEAN", {"default": True}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional":{
                "img_url": ("STRING", {"default": "img_url"}), 
            }
        }

    RETURN_TYPES = ("BOOLEAN","STRING")  
    RETURN_NAMES = ("bool","task_id") 
    FUNCTION = "cogvideox_flash_post" 
    CATEGORY = "dong_tools/cogvideox_flash_post_by_dong" 

    def cogvideox_flash_post(self, prompt, with_audio, is_enable, img_url=None):
        # 获取 API 配置路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        api_path = os.path.join(os.path.dirname(os.path.dirname(script_dir)), "api_by_dong.yaml")

        if not is_enable:
            print("功能已禁用")
            return False, ""

        if not check():
            print("未授权用户")
            return False, ""

        if not os.path.exists(api_path):
            print("API key 文件未找到")
            return False, ""

        # 读取 API key
        with open(api_path, 'r') as file:
            api_keys = yaml.safe_load(file)
        api_key = api_keys.get('zhipuqingyan', {}).get('api_key')

        if not api_key:
            print("API key 未设置")
            return False, ""

        print(f"使用 API key: {api_key}")

        # 初始化 ZhipuAI 客户端
        client = ZhipuAI(api_key=api_key)

        # 发送请求
        try:
            if img_url in [None, "img_url", ""]:
                response = client.videos.generations(
                    model="cogvideox-flash", 
                    prompt=prompt,  
                    with_audio=with_audio,
                )
            else:
                response = client.videos.generations(
                    model="cogvideox-flash", 
                    image_url=img_url,  
                    prompt=prompt,  
                    with_audio=with_audio,
                )

            # 解析返回的 task_id
            if hasattr(response, "id"):
                task_id = response.id  # 获取 ID
            else:
                print("API 响应格式错误:", response)
                return False, ""

            return True, task_id

        except Exception as e:
            print("API 请求失败:", str(e))
            return False, ""

    @classmethod
    def IS_CHANGED(cls, is_enable):
        return True
