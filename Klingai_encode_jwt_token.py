import time
import jwt
import yaml
import os
import re

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")

if not os.path.exists(api_path):
    print("api_key未设置")
    
with open(api_path, 'r') as file:
    api_keys = yaml.safe_load(file)

ak = api_keys['Klingai']['AccessKey_ID']
sk = api_keys['Klingai']['AccessKey_Secret']

def encode_jwt_token():
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 4800,
        "nbf": int(time.time()) - 5 
    }
    token = jwt.encode(payload, sk, headers=headers)
    return token