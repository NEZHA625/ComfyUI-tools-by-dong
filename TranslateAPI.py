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
                "text": ("STRING", {"default": "text"}), 
                "platform": (["Baidu", "Tencent"], {"default":"Tencent"}),  
                "mode": (["zh_to_en", "en_to_zh"], {"default":"en_to_zh"}),  
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")  
    RETURN_NAMES = ("bool", "translation")
    FUNCTION = "translate"  
    CATEGORY = "dong_tools/translate_by_dong"  
    
    def translate(self, text, platform, mode, is_enable):
        if not check():
            print("未授权用户")
            return (False,)
            
        if not is_enable:
            return (False, "wrong", "功能已禁用") 
            
        if not os.path.exists(api_path):
            print("api_key未设置")
            return (False, "api_key未设置", "api_key未设置，请使用set_api节点设置api") 
        
        with open(api_path, 'r') as file:
            api_keys = yaml.safe_load(file)

        def remove_empty_lines_and_merge(text):
            return " ".join([line.strip() for line in text.splitlines() if line.strip() != ""])

        text = remove_empty_lines_and_merge(text)

        def baidu_translate(query, mode):
            appid_or_secretid = api_keys['baidu_translate']['appid_or_secretid']
            secret_key = api_keys['baidu_translate']['secret_key']
            salt = str(random.randint(32768, 65536))  
            # 拼接字符串1，格式：appid + q + salt + 密钥
            query_utf8 = query.encode('utf-8')  # 待翻译文本需要编码为utf-8
            # sign_str = appid_or_secretid + query_utf8.decode('utf-8') + salt + secret_key
            sign_str = str(appid_or_secretid) + query_utf8.decode('utf-8') + str(salt) + secret_key

            # 计算签名 sign，使用MD5加密
            sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
        
            # 构造请求的URL
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
    
        def tencent_translate(query, mode):   
            try:
                with open(api_path, 'r') as file:
                    api_keys = yaml.safe_load(file)
                appid = api_keys['tencent_translate']['appid_or_secretid']
                key = api_keys['tencent_translate']['secret_key']
                print(f"读取到的 appid: {appid}, secret_key: {key}") 
            except Exception as e:
                print(f"读取 API 配置失败: {e}")
                return "error"

            os.environ["TENCENTCLOUD_SECRET_ID"] = appid
            os.environ["TENCENTCLOUD_SECRET_KEY"] = key

            try:
                cred = credential.EnvironmentVariableCredential().get_credential()
                print(f"凭证加载成功，SecretId: {cred.secret_id}, Secret_key: {cred.secret_key}")
            except Exception as e:
                print(f"凭证加载失败: {e}")
                return "error"

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
            print(f"请求参数: {json.dumps(params, indent=2)}") 
            req.from_json_string(json.dumps(params))
            response = client.TextTranslate(req)
            translated_text = str(response.TargetText)
            return translated_text

        if platform == "Baidu":
            result = baidu_translate(text, mode)
            return (True, result)
        if platform == "Tencent":
            result = tencent_translate(text, mode)
            return (True, result)
