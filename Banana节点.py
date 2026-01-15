import os
import json
import base64
import time
import yaml
import requests
import sys
from io import BytesIO
from PIL import Image
import numpy as np
import torch
from torchvision import transforms
import tempfile
from check import check
from _下载图片 import 下载图片
from _kie图床 import kie图床
from _grsai图床 import grsai图床

CYAN  = "\033[36m"
RESET = "\033[0m"

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
api_path = os.path.join(ComfyUI_path, "api_by_dong.yaml")

class Banana节点:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "image3": ("IMAGE",),
                "image4": ("IMAGE",),
                "image5": ("IMAGE",),
                "image6": ("IMAGE",),
                "image7": ("IMAGE",),
                "image8": ("IMAGE",),
                "model": (["nano-banana-pro","nano-banana"],{"default": "nano-banana-pro"}),
                "prompt": ("STRING", {"default": ""}),
                "aspect_ratio": ([
                    "1:1","2:3","3:2","3:4","4:3",
                    "4:5","5:4","9:16","16:9","21:9","auto"
                ], {"default": "auto"}),
                "resolution": (["1K","2K","4K"], {"default": "2K"}),
                "seed": ("INT", {"default": 917724495}),
                "channel": (["kie","suchuang","grsai"], {"default": "grsai"}),
                "img_bed":(["auto","kie","grsai"], {"default": "auto"}),
                "timeout": ("INT", {"default": 600}),
                "kie_api": ("STRING", {"default": ""}), 
                "suchuang_api": ("STRING", {"default": ""}), 
                "grsai_api": ("STRING", {"default": ""}), 
            }
        }

    RETURN_TYPES = ("IMAGE", "BOOLEAN", "STRING")
    RETURN_NAMES = ("image", "state", "log")
    FUNCTION = "run"
    CATEGORY = "dong_tools/nano_banana_by_dong"

    def run(self,model="nano-banana-pro",prompt="",aspect_ratio="auto",resolution="2K",seed=0,channel="grsai",img_bed="auto",timeout=600,kie_api="",suchuang_api="",grsai_api="",**images):
        # -------- 权限检查 --------
        if not check():
            raise RuntimeError("未授权用户")
        
        kie_api_key_final = kie_api.strip() if kie_api else None
        suchuang_api_key_final = suchuang_api.strip() if suchuang_api else None
        grsai_api_key_final = grsai_api.strip() if grsai_api else None
        
        # 如果节点没传，尝试读取 api_by_dong.yaml
        if os.path.exists(api_path):
            api_config = yaml.safe_load(open(api_path, "r", encoding="utf-8"))
            if not kie_api_key_final:
                kie_api_key_final = api_config.get("kie", {}).get("api_key")
            if not suchuang_api_key_final:
                suchuang_api_key_final = api_config.get("suchuang", {}).get("api_key")
            if not grsai_api_key_final:
                grsai_api_key_final = api_config.get("grsai", {}).get("api_key")

        # -------- 上传图片函数 --------
        def upload_image(img, img_bed_type):
            if img is None:
                return None
            if img_bed_type == "kie":
                if not kie_api_key_final:
                    raise ValueError("请提供 kie_api_key")
                return kie图床(kie_api_key_final, img)
            elif img_bed_type == "grsai":
                if not grsai_api_key_final:
                    raise ValueError("请提供 grsai_api_key")
                return grsai图床(grsai_api_key_final, img)
            elif img_bed_type == "auto":
                if grsai_api_key_final:
                    return grsai图床(grsai_api_key_final, img)
                elif kie_api_key_final:
                    return kie图床(kie_api_key_final, img)
                else:
                    raise ValueError("未提供有效 API_KEY")
            else:
                raise ValueError(f"未知图床类型: {img_bed_type}")
       
        # -------- 上传所有图片 --------
        image_urls = []
        for i in range(1, 9):
            img = images.get(f"image{i}")
            if img is not None and img.numel() > 0:
                print(f"检测到 image{i}，开始上传")
                success = False
                for attempt in range(1, 6):  # 最大重试 5 次
                    try:
                        # 临时文件上传
                        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
                            temp_path = tmp_file.name
                        
                            # 如果是 batch tensor，取第一张
                            if img.dim() == 4:
                                img = img[0]
                        
                            # 如果是 (H,W,C)，转成 (C,H,W)
                            if img.dim() == 3 and img.shape[2] in [1,3]:
                                img = img.permute(2,0,1)
                        
                            img_pil = transforms.ToPILImage()(img)
                            img_pil.save(temp_path)
                            # print(f"图片已保存到临时路径: {temp_path}")

                        url = upload_image(temp_path, img_bed)
                        os.remove(temp_path)
        
                        image_urls.append(url)
                        print(f"图片上传成功: {url}")
                        success = True
                        break  # 上传成功，跳出重试循环
        
                    except Exception as e:
                        print(f"图片上传失败，第{attempt}次尝试: {e}")
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                if not success:
                    print(f"图片 image{i} 上传失败，已达到最大重试次数5次")

        # -------- 根据 channel 调用接口 --------
        if channel == "kie":
            # -------- API KEY 获取逻辑 --------
            kie_api_key_final = None
            if kie_api and kie_api.strip():
                kie_api_key_final = kie_api.strip()
                print("使用节点传入的 kie_api_key")
            else:
                if os.path.exists(api_path):
                    with open(api_path, "r", encoding="utf-8") as f:
                        kie_api_key_final = yaml.safe_load(f).get("kie", {}).get("api_key")
                    if kie_api_key_final:
                        print("已从 api_by_dong.yaml 读取 kie_api")
                else:
                    raise ValueError("请填写kie_api_key")
            # -------- 创建任务（KIE） --------
            create_url = "https://api.kie.ai/api/v1/jobs/createTask"
            headers = {"Authorization": f"Bearer {kie_api_key_final}", "Content-Type": "application/json"}
            
            if model == "nano-banana":
                if image_urls:
                    model = "google/nano-banana-edit"
                else:
                    model = "google/nano-banana"
                payload = {
                    "model": model,
                    "input": {
                        "prompt": prompt,
                        "output_format": "png",
                        "image_size": aspect_ratio
                    }
                }
            else:
                payload = {
                    "model": "nano-banana-pro",
                    "input": {
                        "prompt": prompt,
                        "aspect_ratio": aspect_ratio,
                        "resolution": resolution,
                        "output_format": "png",
                    }
                }
                
            if image_urls:
                if model == "google/nano-banana-edit":
                    payload["input"]["image_urls"] = image_urls
                else:
                    payload["input"]["image_input"] = image_urls

            # print("创建任务 payload：")
            # print(json.dumps(payload, ensure_ascii=False, indent=2))

            try:
                r = requests.post(create_url, headers=headers, data=json.dumps(payload), timeout=60)
                result = r.json()
            except Exception as e:
                return (None, False, f"创建任务失败: {str(e)}")

            task_id = (result.get("data") or {}).get("taskId")
            
            if not task_id:
                return (None, False, json.dumps(result, ensure_ascii=False))

            print(f"任务创建成功，task_id={task_id}")

            # -------- kie轮询--------
            poll_interval = 5
            max_retry = max(1, timeout // poll_interval)
            query_url = "https://api.kie.ai/api/v1/jobs/recordInfo"

            for i in range(max_retry):
                # print(f"轮询 {i+1}/{max_retry}")
                try:
                    r = requests.get(query_url, params={"taskId": task_id}, headers=headers, timeout=30)
                    data = r.json().get("data", {})
                except Exception as e:
                    print(f"轮询请求异常: {e}")
                    data = {}

                state = data.get("state")
                
                if state:
                    # print(f"\r轮询 {i+1}/{max_retry} | 状态={state}", end="", flush=True)
                    print(f"{CYAN}\r轮询 {i+1}/{max_retry} | 状态={state}{RESET}", end="", flush=True)

                if state == "success":
                    try:
                        result_urls = json.loads(data.get("resultJson", "{}")).get("resultUrls", [])
                        if result_urls:
                            print(f"\n图片下载地址: {result_urls[0]}")
                            img = 下载图片(result_urls[0])
                            return (img, True, f"生成成功 | task_id={task_id} | 用时≈{poll_interval*(i+1)} 秒")
                    except Exception as e:
                        return (None, False, f"下载图片失败: {e}")

                if state == "fail":
                    fail_msg = data.get("failMsg", "生成失败")
                    return (None, False, fail_msg)

                time.sleep(poll_interval)

            return (None, False, f"超时退出：{timeout} 秒内未完成 | task_id={task_id}")

        elif channel == "suchuang":
            suchuang_api_key_final = None
            if suchuang_api and suchuang_api.strip():
                suchuang_api_key_final = suchuang_api.strip()
                print("使用节点传入的 suchuang_api_key")
            else:
                if os.path.exists(api_path):
                    with open(api_path, "r", encoding="utf-8") as f:
                        suchuang_api_key_final = yaml.safe_load(f).get("suchuang", {}).get("api_key")
                    if suchuang_api_key_final:
                        print("已从 api_by_dong.yaml 读取 suchuang_api")
                else:
                    raise ValueError("请填写suchuang_api_key")
            # -------- 创建任务（Suchuang API） --------
            model_to_url = {
                "nano-banana": "https://api.wuyinkeji.com/api/img/nanoBanana",
                "nano-banana-pro": "https://api.wuyinkeji.com/api/img/nanoBanana-pro"
            }
        
            if model in model_to_url:
                create_url = model_to_url[model]
            else:
                raise ValueError(f"未知的模型: {model}")
        
            headers = {
                "Authorization": suchuang_api_key_final,
                "Content-Type": "application/json;charset:utf-8"
            }
        
            payload = {
                "prompt": prompt,
                "aspectRatio": aspect_ratio,
                "imageSize": resolution,
            }
            
            if model == "nano-banana":
                payload.pop("imageSize", None)
                payload["model"] = "nano-banana"
         
            if image_urls:
                payload["img_url"] = image_urls

            print("创建任务 payload（Suchuang API）：")
            print(json.dumps(payload, ensure_ascii=False, indent=2))

            try:
                r = requests.post(create_url, headers=headers, data=json.dumps(payload), timeout=60)
                result = r.json()
            except Exception as e:
                return (None, False, f"创建任务失败: {str(e)}")

            if result.get("code") != 200 or "data" not in result:
                return (None, False, f"任务创建失败: {json.dumps(result, ensure_ascii=False)}")

            task_id = result["data"].get("id")
            print(f"任务创建成功，task_id={task_id}")

            # -------- 轮询 Suchuang 生成结果 --------
            poll_interval = 5
            max_retry = max(1, timeout // poll_interval)
            query_url = "https://api.wuyinkeji.com/api/img/drawDetail"

            for i in range(max_retry):
                
                try:
                    r = requests.get(
                        query_url,
                        params={"key": suchuang_api_key_final, "id": task_id},
                        headers={"Authorization": suchuang_api_key_final, "Content-Type": "application/json;charset:utf-8"},
                        timeout=30
                    )
                    data = r.json().get("data", {})
                except Exception as e:
                    print(f"轮询请求异常: {e}")
                    data = {}

                status = data.get("status")
                status_dict = {
                                0: "生成中",
                                1: "生成中",
                                2: "成功",
                                3: "失败"
                            }
                # print(f"\r轮询 {i+1}/{max_retry} | 状态={status} ({status_dict.get(status, '未知状态')})", end="", flush=True)
                print(f"{CYAN}\r轮询 {i+1}/{max_retry} | 状态={status} ({status_dict.get(status, '未知状态')}){RESET}", end="", flush=True)
                if status == 2:  # 成功
                    img_url = data.get("image_url")
                    print(f"\n图片下载地址: {img_url}")
                    if img_url:
                        try:
                            img = 下载图片(img_url)
                            return (img, True, f"生成成功 | task_id={task_id} | 用时≈{poll_interval*(i+1)} 秒")
                        except Exception as e:
                            return (None, False, f"下载图片失败: {e}")

                elif status == 3:  # 失败
                    fail_msg = data.get("fail_reason", "生成失败")
                    return (None, False, fail_msg)

                time.sleep(poll_interval)

            return (None, False, f"超时退出：{timeout} 秒内未完成 | task_id={task_id}")

        elif channel == "grsai":
            grsai_api_key_final = None
            if grsai_api and grsai_api.strip():
                grsai_api_key_final = grsai_api.strip()
                print("使用节点传入的 grsai_api_key")
            else:
                if os.path.exists(api_path):
                    with open(api_path, "r", encoding="utf-8") as f:
                        grsai_api_key_final = yaml.safe_load(f).get("grsai", {}).get("api_key")
                    if grsai_api_key_final:
                        print("已从 api_by_dong.yaml 读取 grsai_api")
                else:
                    raise ValueError("请填写grsai_api_key")
            # -------- 创建任务（grsai API） --------
            create_url = "https://grsai.dakka.com.cn/v1/draw/nano-banana"
            headers = {
                "Authorization": f"Bearer {grsai_api_key_final}",
                "Content-Type": "application/json"
            }

            payload = {
                "model":model,
                "prompt": prompt,
                "aspectRatio": aspect_ratio,
                "imageSize": resolution,
                "webHook":"-1",
                "cdn": "zh",
            }
         
            if image_urls:
                payload["urls"] = image_urls

            # print(json.dumps(payload, ensure_ascii=False, indent=2))

            try:
                r = requests.post(create_url, headers=headers, data=json.dumps(payload), timeout=60)
                result = r.json()
            except Exception as e:
                return (None, False, f"创建任务失败: {str(e)}")

            if result.get("code") != 0 or "data" not in result:
                return (None, False, f"任务创建失败: {json.dumps(result, ensure_ascii=False)}")

            task_id = result["data"].get("id")
            print(f"任务创建成功，task_id={task_id}")

            # -------- 轮询 grsai 生成结果 --------
            poll_interval = 5
            max_retry = max(1, timeout // poll_interval)
            query_url = "https://grsai.dakka.com.cn/v1/draw/result"

            for i in range(max_retry):
                # print(f"轮询 {i+1}/{max_retry}")
                try:
                    r = requests.post(query_url, headers=headers, json={"id": task_id}, timeout=30)
                    data = r.json().get("data", {})
                except Exception as e:
                    print(f"轮询请求异常: {e}")
                    data = {}

                state = data.get("status")
                
                if state:
                    # print(f"\r轮询 {i+1}/{max_retry} | 状态={state}", end="", flush=True)
                    print(f"{CYAN}\r轮询 {i+1}/{max_retry} | 状态={state}{RESET}", end="", flush=True)

                if state == "succeeded":
                    try:
                        result_urls = data["results"][0].get("url")
                        if result_urls:
                            print(f"\n图片下载地址: {result_urls}")
                            img = 下载图片(result_urls)
                            return (img, True, f"生成成功 | task_id={task_id} | 用时≈{poll_interval*(i+1)} 秒")
                    except Exception as e:
                        return (None, False, f"下载图片失败: {e}")

                if state == "failed":
                    fail_msg = data.get("failure_reason", "生成失败")
                    return (None, False, fail_msg)

                time.sleep(poll_interval)

            return (None, False, f"超时退出：{timeout} 秒内未完成 | task_id={task_id}")
