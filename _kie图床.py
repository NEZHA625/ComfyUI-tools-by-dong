import requests
import os

def kie图床(api_key, file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    url = "https://kieai.redpandaai.co/api/file-stream-upload"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    file_name = os.path.basename(file_path)

    data = {
        "uploadPath": "images/user-uploads",
        "fileName": file_name
    }

    try:
        with open(file_path, "rb") as f:
            files = {"file": (file_name, f)}
            resp = requests.post(
                url, headers=headers, data=data, files=files, timeout=120
            )
            resp.raise_for_status()
            result = resp.json()
            if not result.get("success"):
                print(f"KIE 上传失败: {result}")
                return None
            return result["data"]["downloadUrl"]

    except Exception as e:
        print(f"KIE 文件上传异常: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    api_key = "a8d438639d8ea798f2a71f9e69f2038c" 
    file_path = r"C:\Users\13672\Desktop\新建文件夹 (2)\微信图片_20260108.jpg"
    try:
        result = upload_file_kie(api_key, file_path)
        print("文件上传成功:", result)
    except Exception as e:
        print(f"错误: {e}")