import os
import time
import yaml

class set_api_Node:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "baidu_appid_or_secretid": ("STRING", {"default": "baidu"}), 
                "baidu_secret_key": ("STRING", {"default": "baidu"}),  
                "siliconflow_api_key": ("STRING", {"default": "https://siliconflow.cn/zh-cn/"}),
                "nvidia_api_key": ("STRING", {"default": "https://build.nvidia.com/"}),
                "zhipu_api_key": ("STRING", {"default": "https://bigmodel.cn/"}),
                "hf_name": ("STRING", {"default": "hf_name"}),
                "hf_key": ("STRING", {"default": "hf_key"}),
            }
        }
    RETURN_TYPES = ("BOOLEAN",) 
    RETURN_NAMES = ("bool",) 
    FUNCTION = "set_api" 
    CATEGORY = "dong_tools/Set_API_by_dong" 

    def set_api(self, baidu_appid_or_secretid, baidu_secret_key, siliconflow_api_key,nvidia_api_key, zhipu_api_key,hf_name,hf_key):

        ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
        custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
        ComfyUI_path = os.path.dirname(custom_node_path)
        api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")
        
        data = {
            "baidu_translate": { 
                "appid_or_secretid": baidu_appid_or_secretid,
                "secret_key": baidu_secret_key
            },
            "siliconflow": { 
                "api_key": siliconflow_api_key
            },
            "nvidia": { 
                "api_key": nvidia_api_key
            },
            "zhipuqingyan": { 
                "api_key": zhipu_api_key
            },
            "huggingface": {
                "hf_name": hf_name,
                "hf_key": hf_key
            }
        }

        with open(api_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
        print(api_path)
        return (True,)
