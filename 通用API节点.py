import requests
import json

class 通用API节点:
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "请求地址": ("STRING", {"default": "https://api.example.com"}),
                "HTTP方法": (["GET", "POST", "PUT", "DELETE"], {"default": "POST"}),
            },
            "optional": {
                "API密钥": ("STRING", {"default": ""}),
                "请求体": ("STRING", {"default": ""}),
                "请求头": ("STRING", {"default": "{}"}),  
                "超时": ("INT", {"default": 10}),
                "节点开关": ("BOOLEAN", {"default": True}),
            }
        }
        
    RETURN_TYPES = ("BOOLEAN","STRING")
    RETURN_NAMES = ("state","response")
    CATEGORY = "dong_tools/http_api_node_by_dong"
    FUNCTION = "run"

    def run(self, 请求地址, HTTP方法, API密钥="", 请求体="", 请求头="{}", 超时=10, 节点开关=True):
        if not 节点开关:
            print("[LOG] 节点未启用")
            return (False, "节点未启用") 

        headers = {}
        if API密钥:
            headers["Authorization"] = f"Bearer {API密钥}"

        if 请求头:
            try:
                custom_headers = json.loads(请求头)
                if isinstance(custom_headers, dict):
                    headers.update(custom_headers)
                else:
                    raise ValueError("请求头必须是 JSON 对象")
            except Exception as e:
                print(f"[LOG] Headers JSON 解析错误: {str(e)}")
                return (False, f"Headers JSON 解析错误: {str(e)}")

        # 解析请求体
        data = None
        if 请求体:
            try:
                data = json.loads(请求体)
            except Exception as e:
                print(f"[LOG] 请求体 JSON 解析错误: {str(e)}")
                return (False, f"请求体 JSON 解析错误: {str(e)}")

        # 打印请求日志
        print(f"[LOG] HTTP 方法: {HTTP方法}")
        print(f"[LOG] 请求地址: {请求地址}")
        print(f"[LOG] Headers: {headers}")
        print(f"[LOG] 请求体: {json.dumps(data, ensure_ascii=False) if data else None}")
        print(f"[LOG] 超时(秒): {超时}")

        try:
            resp = requests.request(
                method=HTTP方法,
                url=请求地址,
                headers=headers,
                json=data,
                timeout=超时
            )
            print(f"[LOG] 响应状态码: {resp.status_code}")
            print(f"[LOG] 响应内容: {resp.text}")

            # 尝试解析 JSON 响应
            try:
                resp_json = resp.json()
                return (True, json.dumps(resp_json, ensure_ascii=False))
            except Exception:
                return (True, resp.text)
        except Exception as e:
            print(f"[LOG] 请求错误: {str(e)}")
            return (False, f"请求错误: {str(e)}")
            
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return True