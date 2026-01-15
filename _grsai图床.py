import requests
import os
import json

# def get_upload_token(api_key, data=None):
#     url = "https://grsai.dakka.com.cn/client/resource/newUploadToken"
#     headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

#     try:
#         response = requests.post(url=url, headers=headers, json=data or {}, timeout=30)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         raise requests.exceptions.RequestException(f"请求失败: {e}")
#     except json.JSONDecodeError as e:
#         raise ValueError(f"响应数据解析失败: {e}")

def get_upload_token_zh(api_key, data=None):
    url = "https://grsai.dakka.com.cn/client/resource/newUploadTokenZH"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        response = requests.post(url=url, headers=headers, json=data or {}, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"grsai 权限校验异常: {e}")
        return None

# def upload_file(api_key, file_path):
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"文件不存在: {file_path}")

#     file_extension = os.path.splitext(file_path)[1].lstrip(".")
#     if not file_extension:
#         file_extension = "png"

#     result = get_upload_token(api_key, {"sux": file_extension})
#     url = result["data"]["url"]
#     key = result["data"]["key"]
#     domain = result["data"]["domain"]

#     try:
#         with open(file_path, "rb") as file:
#             upload_response = requests.put(
#                 url=url,
#                 data=file,
#                 headers={"Content-Type": "application/octet-stream"},
#                 timeout=120
#             )
#             upload_response.raise_for_status()
#             return f"{domain}/{key}"
#     except requests.exceptions.RequestException as e:
#         raise requests.exceptions.RequestException(f"文件上传失败: {e}")
#     except IOError as e:
#         raise IOError(f"文件读取失败: {e}")

def grsai图床(api_key, file_path):
    if not api_key:
        print("grsai 文件上传异常")
        return None
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    file_extension = os.path.splitext(file_path)[1].lstrip(".")
    if not file_extension:
        file_extension = "png"

    result = get_upload_token_zh(api_key, {"sux": file_extension})
    
    if not result or "data" not in result:
        print(f"grsai 获取上传 token 失败: {result}")
        return None
    
    data = result["data"]
    
    if not all(k in data for k in ("token", "key", "url", "domain")):
        print(f"grsai token 数据不完整: {data}")
        return None
    
    token = data["token"]
    key = data["key"]
    url = data["url"]
    domain = data["domain"]


    try:
        with open(file_path, "rb") as file:
            upload_response = requests.post(
                url=url,
                data={"token": token, "key": key},
                files={"file": file},
                timeout=120
            )
            upload_response.raise_for_status()
            return f"{domain}/{key}"
    except Exception as e:
        print(f"grsai 文件上传异常: {e}")
        return None