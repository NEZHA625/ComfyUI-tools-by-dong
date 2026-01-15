class 从文本列表获取文本节点:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文本": ("STRING",),  
                "索引": ("INT",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "get_text_from_list"
    CATEGORY = "dong_tools/get_text_from_list_by_dong"

    def get_text_from_list(self, 文本, 索引):
        if 文本 is None or 文本 == "":
            return ("",)

        # 按换行拆分成列表
        文本列表 = 文本.replace("\r\n", "\n").replace("\r", "\n").split("\n")

        # Python 风格自然索引
        try:
            return (文本列表[索引],)
        except IndexError:
            # 超过范围时返回首行或末行
            if 索引 < 0:
                return (文本列表[0],)
            else:
                return (文本列表[-1],)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return True
