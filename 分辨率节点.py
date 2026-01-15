class 分辨率节点:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "分辨率": ([
                    "512*512", "640*640", "768*768", "1024*1024",
                    "1280*1280", "1536*1536", "2048*2048",
                    "480*720", "720*480", "480*832", "832*480",
                    "512*768", "768*512", "540*832", "832*540",
                    "720*1280", "1280*720", "832*1216", "1216*832",
                    "960*1280", "1280*960", "1024*1536", "1536*1024",
                    "1536*2048", "2048*1536"
                ], {"default": "720*1280"}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("宽", "高")
    FUNCTION = "resolution"
    CATEGORY = "dong_tools/Resolution_by_dong"

    def resolution(self, 分辨率):
        try:
            width, height = 分辨率.split("*")
            return int(width), int(height)
        except Exception:
            print(f"[Resolution_by_dong] 无效分辨率: {分辨率}")
            return 0, 0