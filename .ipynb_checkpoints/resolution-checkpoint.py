import os
from check import check
class ResolutionNode:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "resolution": (["512*512", "768*768", "1024*1024", "1280*1280", "1536*1536", "2048*2048", 
                                "512*768", "768*512", "832*1216", "1216*832", "960*1280", "1280*960", 
                                "1024*1536", "1536*1024", "1536*2048", "2048*1536"], {"default": "960*1280"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "INT", "INT",)  # Returning bool, width, height
    RETURN_NAMES = ("bool", "width", "height")  # Corresponding variable names
    FUNCTION = "resolution" 
    CATEGORY = "dong_tools/Resolution_by_dong"  

    def resolution(self, resolution, is_enable):
        if not check():
            print("未授权用户")
            return (False, 0, 0)
        if not is_enable:
            print("功能已禁用")
            return (False, 0, 0)  # Return False with default width and height (0,0)

        resolution_map = {
            "512*512": (512, 512),
            "768*768": (768, 768),
            "1024*1024": (1024, 1024),
            "1280*1280": (1280, 1280),
            "1536*1536": (1536, 1536),
            "2048*2048": (2048, 2048),
            "512*768": (512, 768),
            "768*512": (768, 512),
            "832*1216": (832, 1216),
            "1216*832": (1216, 832),
            "960*1280": (960, 1280),
            "1280*960": (1280, 960),
            "1024*1536": (1024, 1536),
            "1536*1024": (1536, 1024),
            "1536*2048": (1536, 2048),
            "2048*1536": (2048, 1536)
        }

        # Convert resolution to lowercase to avoid case sensitivity issues
        resolution = resolution.lower()

        if resolution in resolution_map:
            width, height = resolution_map[resolution]
            return (True, width, height)
        else:
            print(f"Invalid resolution: {resolution}")
            return (False, 0, 0)  

