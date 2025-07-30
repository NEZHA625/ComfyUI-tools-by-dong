import os
import io
from volcenginesdkarkruntime import Ark
import yaml
import json
import base64
from PIL import Image, ImageOps, ImageSequence
import torch
from torchvision import transforms
import numpy as np

class doubaoNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api": ("STRING",),  
                "prompt": ("STRING", {"default": "Hello"}),  
                "size": (["1024x1024", "864x1152", "1152x864", "720x1280", "1280x720", "832x1248", "1248x832", "1512x648"], {"default": "720x1280"}),
                "seed": ("INT", {"default": 2048}),
                "guidance_scale": ("FLOAT", {"default": 2.5}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "doubao"
    CATEGORY = "doubao"

    def doubao(self,api, prompt, size, seed, guidance_scale):
        if api=="":
            script_dir = os.path.dirname(os.path.abspath(__file__))
            api_path = os.path.join(os.path.dirname(os.path.dirname(script_dir)), "api_by_dong.yaml")
            with open(api_path, 'r') as file:
                api_keys = yaml.safe_load(file)
            api_key = api_keys['doubao']['api_key']
        else:
            api_key = api
        base_url = "https://ark.cn-beijing.volces.com/api/v3"
        client = Ark(
            base_url=base_url,
            api_key=api_key,
        )

        imagesResponse = client.images.generate(
            model="doubao-seedream-3-0-t2i-250415",
            prompt=prompt,
            size=size,
            seed=seed,
            guidance_scale=guidance_scale,
            watermark=False,
            response_format= "b64_json"
        )
        result = imagesResponse.data[0].b64_json
        decoded_data = base64.b64decode(result)
        
        img = Image.open(io.BytesIO(decoded_data))
        img_out = []
        for frame in ImageSequence.Iterator(img):
            frame = ImageOps.exif_transpose(frame)
            if frame.mode == "I":
                frame = frame.point(lambda i: i * (1 / 256)).convert("L")
            image = frame.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image).unsqueeze(0)
            img_out.append(image)
        img_out = img_out[0]
        return (img_out,)