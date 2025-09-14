class get_text_from_list_Node:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_list": ("STRING",), 
                "index": ("INT",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "get_text_from_list"
    CATEGORY = "dong_tools/get_text_from_list_by_dong"

    def get_text_from_list(self, text_list, index):
        # 防止索引越界
        if index < 0 or index >= len(text_list):
            return ""  # 或者返回 None
        return (text_list[index],)
