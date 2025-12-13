import time
import requests
import yaml
import os
from check import check

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")

class suchuang_get_node:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "task_id": ("STRING", {"default": ""}),
                "poll_interval": ("FLOAT", {"default": 5.0}),  # 轮询间隔秒
                "timeout_sec": ("INT", {"default": 600, "min": 1, "max": 3600}),  # 最大等待时间秒
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("image_url",)
    FUNCTION = "get_image_url"
    CATEGORY = "dong_tools/suchaung_nano_get_by_dong"

    def get_image_url(self, task_id, poll_interval=2.0, timeout_sec=600):
        # --- 权限检查 ---
        if not check():
            return ("未授权用户",)

        # --- API KEY 检查 ---
        if not os.path.exists(api_path):
            return ("api_key未设置，请使用 set_api 节点设置 api",)

        with open(api_path, "r") as file:
            api_keys = yaml.safe_load(file)
        api_key = api_keys["suchuang"]["api_key"]

        # --- 接口 URL & headers ---
        url = "https://api.wuyinkeji.com/api/img/drawDetail"
        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json;charset=utf-8"
        }

        elapsed_time = 0.0

        while elapsed_time < float(timeout_sec):
            try:
                res = requests.get(url, params={"id": task_id}, headers=headers, timeout=10).json()
                code = res.get("code")
                data = res.get("data", {})
                status = data.get("status")

                if code != 200:
                    return (f"接口返回错误: {res}",)

                # 生成成功
                if status == 2:
                    return (data.get("image_url", ""),)

                # 生成失败
                elif status == 3:
                    return (f"任务生成失败，原因: {data.get('fail_reason','未知')}",)

                # 生成中或排队中
                time.sleep(poll_interval)
                elapsed_time += poll_interval

            except Exception as e:
                return (f"请求异常: {str(e)}",)

        return ("等待超时，任务未完成",)
