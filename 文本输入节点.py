class 文本输入节点:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text": ("STRING", {"multiline": True})}}
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "txt"
    CATEGORY = "dong_tools/text_by_dong"

    def txt(self, text):
        return (text,)