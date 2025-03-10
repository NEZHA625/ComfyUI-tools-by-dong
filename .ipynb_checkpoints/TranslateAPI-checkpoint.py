import os
import time
import hashlib
import urllib.parse
import requests
import random
import re
import yaml
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
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "text": ("STRING", {"default": "source_directory"}), 
                "platform": (["Baidu", "Tencent"], {"default":"Baidu"}),  
                "mode": (["zh_to_en", "en_to_zh"], {"default":"en_to_zh"}),  
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING")  # 返回类型是布尔值
    RETURN_NAMES = ("bool", "translation", "log")  # 返回变量名是bool
    FUNCTION = "translate"  # 执行的入口方法
    CATEGORY = "dong_tools/translate_by_dong"  # 分类，决定显示在哪一类节点下
    
    def translate(self, text, platform, mode, is_enable):
        if not check():
            print("未授权用户")
            return (False,)
        if not is_enable:
            return (False, "wrong", "功能已禁用")  # 如果禁用，则返回 False

        if not os.path.exists(api_path):
            print("api_key未设置")
            return (False, "api_key未设置", "api_key未设置，请使用set_api节点设置api") 
        
        with open(api_path, 'r') as file:
            api_keys = yaml.safe_load(file)

        def remove_empty_lines_and_merge(text):
            # 删除所有空行，并将所有文本合并成一行
            return " ".join([line.strip() for line in text.splitlines() if line.strip() != ""])

        # 示例使用
        text = remove_empty_lines_and_merge(text)

        
        def baidu_translate(query, mode):
            """
            使用百度翻译API进行翻译
            :param appid: 百度翻译API的APPID
            :param secret_key: 百度翻译API的密钥
            :param query: 待翻译的文本
            :param mode: 翻译模式（如zh_to_en）
            :return: 翻译结果（字典格式）
            """
            appid_or_secretid = api_keys['baidu_translate']['appid_or_secretid']
            secret_key = api_keys['baidu_translate']['secret_key']
            
            # 生成随机数 salt
            salt = str(random.randint(32768, 65536))  # 随机数范围在[32768, 65536]
            
            # 拼接字符串1，格式：appid + q + salt + 密钥
            query_utf8 = query.encode('utf-8')  # 待翻译文本需要编码为utf-8
            # sign_str = appid_or_secretid + query_utf8.decode('utf-8') + salt + secret_key
            sign_str = str(appid_or_secretid) + query_utf8.decode('utf-8') + str(salt) + secret_key

            # 计算签名 sign，使用MD5加密
            sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
        
            # 构造请求的URL
            base_url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
            from_lang, to_lang = mode.split("_to_")  # 从模式中提取源语言和目标语言
            params = {
                "q": query,
                "from": from_lang,  # 源语言（如zh）
                "to": to_lang,      # 目标语言（如en）
                "appid": appid_or_secretid,
                "salt": salt,
                "sign": sign
            }
        
            response = requests.get(base_url, params=params)
            if response.status_code != 200:
                return {"error_code": "request_error", "error_msg": "Request failed"}
            result = response.json()  # 转换成JSON格式
            
            if "error_code" in result:
                return {"error_code": result["error_code"], "error_msg": result.get("error_msg", "Unknown Error")}
            
            # 返回翻译结果
            return result["trans_result"][0]["dst"]
    
        def tencent_translate(query, mode):
            appid_or_secretid = api_keys['tencent_translate']['appid_or_secretid']
            secret_key = api_keys['tencent_translate']['secret_key']
            # print("未完待定，这个以后再写")
            # return (False,"未完待定，这个以后再写","未完待定，这个以后再写")

        # 根据平台选择翻译方式
        if platform == "Baidu":
            result = baidu_translate(text, mode)
            return (True, result, "百度翻译成功")
        if platform == "Tencent":
            # result = tencent_translate(text, mode)
            return (False, "未完待定，这个以后再写", "腾讯翻译未完成")
