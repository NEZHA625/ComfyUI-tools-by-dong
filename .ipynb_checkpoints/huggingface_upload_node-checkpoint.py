from huggingface_hub import HfApi
import os
import time
import yaml
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from check import check
ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)

api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")
class HuggingFaceUploadNode:

    def __init__(self):
        self.uploader = HuggingFaceUploader()

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "model_id": ("STRING", {"default": "your_model_id"}),  # 默认模型ID
                "upload_path": ("STRING", {"default": "path_to_your_file"}),  # 上传文件路径
                "is_mirror": ("BOOLEAN", {"default": True}),  # 是否使用镜像
                "is_enable": ("BOOLEAN", {"default": False}),  # 是否启用上传功能
            }
        }
    RETURN_TYPES = ("STRING","BOOLEAN")  # 返回类型是布尔值
    RETURN_NAMES = ("log","bool")  # 返回变量名是bool
    FUNCTION = "upload_to_huggingface"
    CATEGORY = "dong_tools/Upload_to_huggingface"

    def upload_to_huggingface(self, model_id, upload_path, is_mirror, is_enable):
        if not check():
            print("未授权用户")
            return (False,)
        if not is_enable:
            return ("上传功能已禁用",)
        if not os.path.exists(api_path):
            print("api_key未设置")
            return ("api_key未设置", "api_key未设置，请使用set_api节点设置api",False) 
        else:
            with open(api_path, 'r') as file:
                api_keys = yaml.safe_load(file)
            username = api_keys['huggingface']['hf_name']
            user_token = api_keys['huggingface']['hf_key']
            return self.uploader.upload_to_huggingface(username, model_id, user_token, upload_path, is_mirror, is_enable)


class HuggingFaceUploader:
    def upload_to_huggingface(self, username, model_id, user_token, upload_path, is_mirror, is_enable):

        if not is_enable:
            return ("上传功能已禁用",)

        try:
            hf_endpoint = "https://huggingface"+".co" if not is_mirror else "https://hf-mirror.com"
            api = HfApi(endpoint=hf_endpoint, token=user_token)

            # 模型库 ID
            model_repo = f"{username}/{model_id}"

            # 检查或创建仓库
            error_message = self.check_or_create_repo(api, model_repo)
            if error_message:
                return (error_message,)

            # 上传文件
            return self.upload_files(api, upload_path, model_repo)

        except Exception as e:
            return self.upload_files(api, upload_path, model_repo)

    def check_or_create_repo(self, api, model_repo):
        """
        检查仓库是否存在，如果不存在则创建。
        """
        try:
            api.repo_info(model_repo)
            print(f"模型库 {model_repo} 已存在")
            return None
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"模型库 {model_repo} 不存在，正在创建...")
                api.create_repo(model_repo, private=False, exist_ok=True)
                return None
            elif e.response.status_code == 403:
                error_message = f"访问被拒绝：你没有权限访问仓库 {model_repo}。"
                print(error_message)
                return error_message
            else:
                raise e

    def upload_files(self, api, upload_path, model_repo):
        """
        上传文件或文件夹到 Hugging Face 模型库
        """
        print(f"开始上传文件到 HuggingFace 模型库: {model_repo}...")

        retries = 3
        for attempt in range(retries):
            try:
                if os.path.isdir(upload_path):
                    api.upload_folder(folder_path=upload_path, repo_id=model_repo, repo_type="model")
                else:
                    api.upload_file(path_or_fileobj=upload_path, repo_id=model_repo, repo_type="model")

                print(f"文件上传成功到: {model_repo}")
                # return (f"文件成功上传至 HuggingFace: {model_repo}",)
                return (f"success",True)

            except requests.exceptions.RequestException as e:
                error_message = f"请求失败: {e}"
                print(error_message)
                if attempt < retries - 1:
                    print(f"等待 {2 ** attempt} 秒后重试...")
                    time.sleep(2 ** attempt)  # 指数退避策略
                else:
                    return (error_message,False)

    @classmethod
    def IS_CHANGED(cls, model_id, upload_path, is_mirror, is_enable):
        return True
