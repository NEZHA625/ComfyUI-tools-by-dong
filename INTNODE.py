from check import check

class INTNODE:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "INT": ([1, 2, 3, 4], {"default": 1}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("INT","BOOLEAN")
    RETURN_NAMES = ("int","bool")
    FUNCTION = "choose_int"
    CATEGORY = "dong_tools/int_by_dong"

    def choose_int(self, INT, is_enable):
        if not is_enable:
            print("功能已禁用")
            return (None,)

        if not check():
            print("未授权用户")
            return (None,)

        return (INT,True)
