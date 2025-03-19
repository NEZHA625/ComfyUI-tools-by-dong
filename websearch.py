import os
import time
import requests
import uuid
import base64

class web_search_Node:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "prompt": ("STRING",), 
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN","STRING")  
    RETURN_NAMES = ("bool","text") 
    FUNCTION = "web_search" 
    CATEGORY = "dong_tools/web_search_by_dong" 

    def web_search(self, prompt, is_enable):

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

        if not api_key:
            print("API key 未设置")
            return False, None
            
        with open(api_path, 'r') as file:
            api_keys = yaml.safe_load(file)
            
        api_key = api_keys.get('zhipuqingyan', {}).get('api_key')
        
        msg = [
            {
                "role": "user",
                "content":prompt
            }
        ]
        tool = "web-search-pro"
        url = "https://open.bigmodel.cn/api/paas/v4/tools"
        request_id = str(uuid.uuid4())
        data = {
            "request_id": request_id,
            "tool": tool,
            "stream": False,
            "messages": msg
        }
    
        resp = requests.post(
            url,
            json=data,
            headers={'Authorization': api_key},
            timeout=300
        )
        print(resp.content.decode())


