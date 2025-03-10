import winsound
import os

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
any = AnyType("*")

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
notice_path = os.path.join(ComfyUI_tools_by_dong_path, "notice.wav")

class Notice_Node:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "any": (any,),
                "is_enable": ("BOOLEAN", {"default": False}),
            }
        }

    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)
    OUTPUT_NODE = True
    RETURN_TYPES = (any,)
    RETURN_NAMES = ("result",)  
    FUNCTION = "music"  
    CATEGORY = "dong_tools/notice_by_dong" 

    def music(self, any, is_enable):
        
        print(is_enable)
        if not is_enable[0]:
            return (any,)
        else:
            try:
                winsound.PlaySound(notice_path, winsound.SND_FILENAME)
            except Exception as e:
                pass
            return (any,)

        
    @classmethod
    def IS_CHANGED(cls):
        return (True,)

        






