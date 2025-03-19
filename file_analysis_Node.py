import os
import time
from zhipuai import ZhipuAI
from pathlib import Path
import json
from check import check
import yaml

class file_analysis_Node:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "prompt": ("STRING", {"default": "结合内容进行分析"}), 
                "file_path": ("STRING", {"default": "file_path"}),  
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN","STRING")  
    RETURN_NAMES = ("bool","text") 
    FUNCTION = "file_extract" 
    CATEGORY = "dong_tools/file_extract_by_dong" 

    def file_extract(self,prompt,file_path,is_enable):

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

        # 读取 API Key
        with open(api_path, 'r') as file:
            api_keys = yaml.safe_load(file)
        api_key = api_keys.get('zhipuqingyan', {}).get('api_key')

        if not api_key:
            print("API key 未设置")
            return False, None

        client = ZhipuAI(api_key=api_key)

        # 格式限制：.PDF .DOCX .DOC .XLS .XLSX .PPT .PPTX .PNG .JPG .JPEG .CSV .PY .TXT .MD .BMP .GIF
        # 大小：单个文件50M、总数限制为100个文件
        
        file_object = client.files.create(file=Path(file_path), purpose="file-extract")
        
        # 获取文本内容
        file_content = json.loads(client.files.content(file_id=file_object.id).content)["content"]
        
        # 生成请求消息
        message_content = f"结合\n{file_content}\n的内容，{prompt}"
        
        response = client.chat.completions.create(
            model="glm-4-flash",  
            messages=[
                {"role": "user", "content": message_content}
            ],
        )
        
        content = response.choices[0].message.content
        
        return(True,content)

    @classmethod
    def IS_CHANGED(cls, is_enable):
        return True