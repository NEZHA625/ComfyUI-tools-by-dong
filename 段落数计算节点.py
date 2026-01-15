class 段落数计算节点:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文本": ("STRING",),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("数量",)
    FUNCTION = "计算文本段落数"
    CATEGORY = "dong_tools/count_paragraph_by_dong"

    def 计算文本段落数(self, 文本):
        if 文本 is None:
            return (0,)

        # 统一换行符
        text = 文本.replace("\r\n", "\n").replace("\r", "\n")

        # 每一行都算一个段落（包括空行、结尾空行）
        lines = text.split("\n")

        return (len(lines),)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return True