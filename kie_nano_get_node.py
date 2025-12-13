import requests
import json
import yaml
import os
import time
from check import check


ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")


class kie_nano_get_node:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "task_id": ("STRING", ),
                "poll_interval": ("INT", {"default": 5, "min": 1, "max": 60}),
                "timeout_sec": ("INT", {"default": 600, "min": 1, "max": 3600}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("state", "image_url", "raw_json")
    FUNCTION = "query_task"
    CATEGORY = "dong_tools/nano_get_by_dong"

    def query_task(self, task_id, poll_interval, timeout_sec):

        # --- 授权检查 ---
        if not check():
            return ("未授权用户", "", "")

        # --- API KEY 检查 ---
        if not os.path.exists(api_path):
            return ("api_key未设置，请使用set_api节点设置api", "", "")

        with open(api_path, "r") as file:
            api_keys = yaml.safe_load(file)
        api_key = api_keys["kie"]["api_key"]

        url = "https://api.kie.ai/api/v1/jobs/recordInfo"
        headers = {"Authorization": f"Bearer {api_key}"}

        start_time = time.time()

        while True:
            # 超时判断
            if time.time() - start_time > timeout_sec:
                return ("timeout", "", f"超过 {timeout_sec} 秒未完成任务")

            try:
                response = requests.get(url, headers=headers, params={"taskId": task_id})
                result = response.json()

                # API 调用失败
                if result.get("code") != 200:
                    return ("error", "", json.dumps(result, ensure_ascii=False))

                data = result.get("data", {})
                state = data.get("state", "")

                # 任务仍在进行中
                if state in ["waiting", "queuing", "generating"]:
                    time.sleep(poll_interval)
                    continue

                # 任务成功
                if state == "success":
                    result_json = json.loads(data.get("resultJson", "{}"))
                    url_list = result_json.get("resultUrls", [])
                    image_url = url_list[0] if url_list else ""
                    return ("success", image_url, json.dumps(result, ensure_ascii=False))

                # 任务失败
                if state == "fail":
                    return ("fail", "", json.dumps(result, ensure_ascii=False))

                # 其它未知状态
                return (state, "", json.dumps(result, ensure_ascii=False))

            except Exception as e:
                return ("error", "", str(e))
