import os
import time
import hashlib
import urllib.parse
import requests
import random
import re
import yaml
import json
from tencentcloud.common import credential
from tencentcloud.tmt.v20180321 import tmt_client, models
from check import check

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")

class TranslateAPINode:
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING",{"multiline": True}),
                "mode": (["zh_to_en", "en_to_zh"], {"default":"en_to_zh"})
            }
        }

    RETURN_TYPES = ("STRING",)  
    RETURN_NAMES = ("text",)
    FUNCTION = "translate"  
    CATEGORY = "dong_tools/translate_by_dong" 
    
    def translate(self, text, mode):
        if text == "":
            return (text,)
        if not re.search(r'[A-Za-z]', text) and mode == "en_to_zh":
            return (text,)
        elif not re.search(r'[\u4e00-\u9fff]', text) and mode == "zh_to_en":
            return (text,)
            
        if not check():
            print("未授权用户")
            return ("未授权用户",)
    
        if not os.path.exists(api_path):
            print("api_key未设置")
            return (text,)
    
        with open(api_path, 'r', encoding='utf-8') as file:
            api_keys = yaml.safe_load(file)
    
        def remove_empty_lines_and_merge(text):
            return " ".join([line.strip() for line in text.splitlines() if line.strip() != ""])
    
        text = remove_empty_lines_and_merge(text)
    
        def baidu_translate(query, appid_or_secretid, secret_key, mode):
            salt = str(random.randint(32768, 65536))
            sign_str = str(appid_or_secretid) + query + str(salt) + secret_key
            sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
            print("\033[38;5;214m[Translate Node] 百度翻译\033[0m")
            base_url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
            from_lang, to_lang = mode.split("_to_")
            params = {
                "q": query,
                "from": from_lang,
                "to": to_lang,
                "appid": appid_or_secretid,
                "salt": salt,
                "sign": sign
            }
            response = requests.get(base_url, params=params)
            if response.status_code != 200:
                return {"error_code": "request_error", "error_msg": "Request failed"}
            result = response.json()
    
            if "error_code" in result:
                return {"error_code": result["error_code"], "error_msg": result.get("error_msg", "Unknown Error")}
            return result["trans_result"][0]["dst"]
    
        def tencent_translate(query, appid, key, mode):
            try:
                os.environ["TENCENTCLOUD_SECRET_ID"] = appid
                os.environ["TENCENTCLOUD_SECRET_KEY"] = key
                cred = credential.EnvironmentVariableCredential().get_credential()
            except Exception as e:
                print(f"腾讯云凭证加载失败: {e}")
                return "error"
            print("\033[38;5;214m[Translate Node] 腾讯翻译\033[0m")
            from_lang, to_lang = mode.split("_to_")
            region = "ap-shanghai"
            client = tmt_client.TmtClient(cred, region)
            req = models.TextTranslateRequest()
            params = {
                "SourceText": query,
                "Source": from_lang,
                "Target": to_lang,
                "ProjectId": 0
            }
            req.from_json_string(json.dumps(params))
            response = client.TextTranslate(req)
            return str(response.TargetText)
    
        # 优先使用腾讯翻译
        if 'tencent_translate' in api_keys and \
           api_keys['tencent_translate'].get('appid_or_secretid') and \
           api_keys['tencent_translate'].get('secret_key'):
            translated_text = tencent_translate(
                text,
                api_keys['tencent_translate']['appid_or_secretid'],
                api_keys['tencent_translate']['secret_key'],
                mode
            )
            return (translated_text,)
    
        # 再尝试百度翻译
        elif 'baidu_translate' in api_keys and \
             api_keys['baidu_translate'].get('appid_or_secretid') and \
             api_keys['baidu_translate'].get('secret_key'):
            translated_text = baidu_translate(
                text,
                api_keys['baidu_translate']['appid_or_secretid'],
                api_keys['baidu_translate']['secret_key'],
                mode
            )
            return (translated_text,)
    
        else:
            print("没有找到可用的翻译API配置")
            return (text,)
