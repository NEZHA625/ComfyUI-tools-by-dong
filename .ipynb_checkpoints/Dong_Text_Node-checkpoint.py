class Dong_Text_Node:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text": ("STRING", {"multiline": True})}}
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "txt"
    CATEGORY = "dong_tools"

    def txt(self, text):
        return (text,)