import xml.etree.ElementTree as ET
import time
import hashlib
from datetime import datetime
import pytz
import requests
import logging
from openai import OpenAI
import yaml
import os
import re
from check import check

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")

class LLM_Node:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (["glm-4-flash", "siliconflow", "nvidia"], {"default": "glm-4-flash"}),  
                "system_prompt": ("STRING", {"default": "default"}),
                "user_prompt": ("STRING", {"default": "default"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "Translate_mode": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "siliconflow_model": (["DeepSeek-R1","DeepSeek-V3","DeepSeek-R1-Distill-Llama-70B","DeepSeek-R1-Distill-Qwen-32B","DeepSeek-R1-Distill-Qwen-14B","free-DeepSeek-R1-Distill-Llama-8B","free-DeepSeek-R1-Distill-Qwen-7B","free-DeepSeek-R1-Distill-Qwen-1.5B"], {"default":"DeepSeek-R1"}),
                "nvidia_model": (["DeepSeek-R1"], {"default": "DeepSeek-R1"}),
            }
        }
        
    RETURN_TYPES = ("BOOLEAN", "STRING",) 
    RETURN_NAMES = ("bool", "answer",) 
    FUNCTION = "LLM"
    CATEGORY = "dong_tools/LLM_by_dong"  

    def LLM(self, model, system_prompt, user_prompt, is_enable, Translate_mode,siliconflow_model, nvidia_model):
        if not check():
            print("未授权用户")
            return (False,)
        
        if not is_enable:
            return "功能已禁用"
    
        if not os.path.exists(api_path):
            print("api_key未设置")
            return "api_key未设置，请使用set_api节点设置api"
    
        with open(api_path, 'r') as file:
            api_keys = yaml.safe_load(file)
            
        if system_prompt == "default":
            system_prompt = "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"            
        if Translate_mode:
            system_prompt = "你是一个翻译专家，如果我给你的是中文，请你将它翻译成地道的英文，如果我给你的是英文，翻译成地道的中文。"

        def glm_4_flash():
            api_key = api_keys['zhipuqingyan']['api_key']
            api_url = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
            headers = {
                'Authorization': api_key,
                'Content-Type': 'application/json'
            }
            data = {
                "model": "glm-4-flash",
                "messages": [{"role": "system", "content": system_prompt},{"role": "user", "content": user_prompt}],
                "max_tokens":4095
            }
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()  
            response_data = response.json()
            return response_data['choices'][0]['message']['content']

        def siliconflow():
            api_key = api_keys['siliconflow']['api_key'] 
            url = "https://api.siliconflow.cn/v1/chat/completions"
            
            model_to_use = siliconflow_model 
            model_to_use = model_to_use.replace('free-', '')
            select_model = "deepseek-ai/" + model_to_use
            print("\n"+select_model)

            payload = {
                "model": select_model,
                "messages": [{"role": "system", "content": system_prompt},{"role": "user", "content": user_prompt}],
                "stream": False,
                "max_tokens": 8192,
                "stop": ["null"],
                "temperature": 0.7,
                "top_p": 0.7,
                "top_k": 50,
                "frequency_penalty": 0.5,
                "n": 1,
                "response_format": {"type": "text"},
            }
            headers = {
                "Authorization": "Bearer " + api_key,
                "Content-Type": "application/json"
            }
            try:
                response_data = requests.post(url, json=payload, headers=headers)
                response_data.raise_for_status()  
                response_json = response_data.json()
                if "R1" in select_model and "1.5B" not in select_model:
                    reasoning_content = response_json["choices"][0]["message"]["reasoning_content"]
                    print(f"\nthink:\n{reasoning_content}\n")
                    use_token = response_json["usage"]["total_tokens"]
                    print(f"\n使用token数：{use_token}\n")
                return response_json['choices'][0]['message']['content']
            except requests.exceptions.RequestException as e:
                print(f"请求失败: {e}")
                return None
            
        def nvidia():
            api_key = api_keys['nvidia']['api_key']
            
            model_to_use = nvidia_model
            select_model = "deepseek-ai/" + model_to_use
            select_model = select_model.lower()
            print("\n"+select_model)
            
            client = OpenAI(
              base_url="https://integrate.api.nvidia.com/v1",
              api_key = api_key
            )
            completion = client.chat.completions.create(
              model=select_model,
              messages=[{"role": "system", "content": system_prompt},{"role": "user", "content": user_prompt}],
              temperature=0.6, 
              top_p=0.7, 
              max_tokens=8192, 
              stream=False  
            )
            
            response_data=(completion.choices[0].message.content)
            print(response_data)
            
            pattern = r'<think>(.*?)</think>'
            matches = re.findall(pattern, response_data, flags=re.DOTALL)
            if matches:
                think_content = matches[0]
                print(f"\nThink:\n{think_content}")
            else:
                print("No <think>")
                
            use_token = completion.usage.total_tokens
            print(f"\n使用token数：{use_token}\n")
            
            unswer_content = re.sub(pattern, '', response_data, flags=re.DOTALL).lstrip('\n')
            return unswer_content
            
        if model == "glm-4-flash":
            return (True, glm_4_flash())
        elif model == "siliconflow":
            return (True, siliconflow())
        elif model == "nvidia":
            return (True, nvidia())       
        else:
            return (False, "不支持的模型类型")
            
    @classmethod
    def IS_CHANGED(cls):
        return True