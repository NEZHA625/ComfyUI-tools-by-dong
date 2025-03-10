class PromptConcatNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "delimmitor": (["none", "space", "comma"], {"default": "none"}),
            },
            "optional": {
                "text1": ("STRING", {"forceInput": True}),
                "text2": ("STRING", {"forceInput": True}),
                "text3": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "value"
    CATEGORY = "dong_tools/Prompt_concat_by_dong"

    def value(self, delimmitor, text1=None, text2=None, text3=None):
        
        needdelim = False
        a = ""  
        
        if delimmitor == "space":
            a = " "
        elif delimmitor == "comma":
            a = ", "

        concatenated = ""

        if text1:
            concatenated = text1
            needdelim = True
        
        if text2:
            if needdelim:
                concatenated += a
            concatenated += text2
            needdelim = True
        
        if text3:
            if needdelim:
                concatenated += a
            concatenated += text3
            needdelim = True

        return (concatenated,)
