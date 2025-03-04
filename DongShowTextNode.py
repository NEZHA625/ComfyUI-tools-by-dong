class DongShowTextNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            }
        }
    
    INPUT_IS_LIST = True
    RETURN_TYPES = ("Text",)
    RETURN_NAMES = ("text",)
    FUNCTION = "show"
    CATEGORY = "dong_tools/show_text_by_dong"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)

    def show(self, text):
        return {"ui": {"text": text}, "result": (text,)}