from check import check


class AlwaysEqualProxy(str):
    def __eq__(self, _):
        return True

    def __ne__(self, _):
        return False


any_type = AlwaysEqualProxy("*")


class 获取视频路径节点:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "data": (any_type,),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("mp4_path",)
    FUNCTION = "get_mp4"
    CATEGORY = "dong_tools/Data_handle_by_dong"

    def get_mp4(self, data, is_enable):
        # 授权校验
        if not check():
            print("未授权用户")
            return ("",)

        if not is_enable:
            print("GetMP4Path 功能已禁用")
            return ("",)

        """
        支持的 data 形态：
        1) [bool, [files...]]
        2) [[bool, [files...]]]
        3) [files...]
        """

        # —— 解 batch —— #
        if isinstance(data, (list, tuple)) and len(data) == 1:
            data = data[0]

        files = None

        # —— 标准 ComfyUI 输出 —— #
        if isinstance(data, (list, tuple)) and len(data) >= 2:
            if isinstance(data[1], (list, tuple)):
                files = data[1]

        # —— 直接是文件列表 —— #
        if files is None and isinstance(data, (list, tuple)):
            files = data

        if not isinstance(files, (list, tuple)):
            return ("",)

        # 1️⃣ 优先 audio mp4
        for f in files:
            if isinstance(f, str) and f.lower().endswith(".mp4") and "audio" in f.lower():
                return (f,)

        # 2️⃣ 再找任意 mp4
        for f in files:
            if isinstance(f, str) and f.lower().endswith(".mp4"):
                return (f,)

        # 3️⃣ 没有就返回空
        return ("",)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return True