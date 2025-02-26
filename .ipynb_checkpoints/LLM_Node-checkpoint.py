import xml.etree.ElementTree as ET
import time
import hashlib
from datetime import datetime
import pytz
import requests
import logging
from openai import OpenAI

class LLM_Node:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "model": (["glm-4", "doubao"], {"default": "glm-4"}),  
                "api_key": ("STRING", {"default": "api_key"}), 
                "system_prompt": ("STRING", {"default": "default"}),
                "user_prompt": ("STRING", {"default": "default"}),
                "is_enable": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "doubao_model_id": ("STRING", {"default": "model_id"}),
                "glm_model": (["glm-4","glm-4-flash"], {"default": "glm-4-flash"}),
                
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING")  # 返回类型是布尔值
    RETURN_NAMES = ("bool", "answer", "log")  # 返回变量名是bool
    FUNCTION = "LLM"  # 执行的入口方法
    CATEGORY = "dong_tools/LLM_by_dong"  

    def LLM(self, model, api_key, system_prompt, user_prompt, is_enable, doubao_model_id, glm_model):
        if not is_enable:
            print("功能已禁用")
            return (False, "", "功能已禁用")  # 如果禁用，则返回 False
        
        # glm-4
        def glm_4():
            api_url = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
            headers = {
                'Authorization': api_key,
                'Content-Type': 'application/json'
            }
            if system_prompt == "default":
                prompt = "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"
            else:
                prompt = system_prompt
            data = {
                "model": glm_model,
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }
            try:
                response = requests.post(api_url, headers=headers, json=data)
                response.raise_for_status()  # 如果响应状态码不是 2xx，将抛出异常
                response_data = response.json()
                return response_data['choices'][0]['message']['content']
            except requests.exceptions.RequestException as e:
                logging.error(f"请求失败: {e}")
                return "请求失败，请联系H917724495。\n 前往https://bigmodel.cn/获取API_key"
            except KeyError as e:
                logging.error(f"AI返回格式错误: {e}")
                return "接口返回数据格式错误，请稍后再试。"

        # Doubao-pro-32k
        def Doubao_pro_32k():
            if system_prompt == "default":
                prompt = "你是豆包，是由字节跳动开发的 AI 人工智能助手"
            else:
                prompt = system_prompt

            if doubao_model_id == "default":
                return (False, "", "请输入豆包模型id")
            
            client = OpenAI(
                api_key=api_key,
                base_url="https://ark.cn-beijing.volces.com/api/v3",
            )
            try:
                completion = client.chat.completions.create(
                    model = doubao_model_id, 
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                return True, completion.choices[0].message.content, "请求成功"
            except Exception as e:
                logging.error(f"请求失败: {e}")
                return False, "", "处理请求时发生错误，请稍后再试。"

        # 根据选择的模型执行
        if model == "glm-4":
            return (True, glm_4(), "GLM请求成功")
        elif model == "doubao":
            return (True, Doubao_pro_32k(), "Doubao请求成功")
        else:
            return (False, "", "不支持的模型类型")

    @classmethod
    def IS_CHANGED(cls, is_enable):
        """
        判断节点配置是否有变化。
        """
        return True
