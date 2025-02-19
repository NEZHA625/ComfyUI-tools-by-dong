import os
import uuid
import sys
# current_script_path = os.path.dirname(os.path.abspath(__file__))
# custom_nodes_path = os.path.join(current_script_path)
# sys.path.append(custom_nodes_path)
from check import check

ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)
Authorization_path = os.path.join(ComfyUI_path, "Authorization.txt")

class SetAppidNode:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Verification": ("STRING", {"default": "Verification_code"}), 
            }
        }

    RETURN_TYPES = ("STRING",) 
    RETURN_NAMES = ("result",) 
    FUNCTION = "Authorization"  
    CATEGORY = "dong_tools/Authorization"

    def Authorization(self, Verification):
        def temp_uuid():
            return str(uuid.uuid1())
        x = temp_uuid()[-6:-2]

        if Verification == "Verification_code":
            print("\n未授权用户\n")
            print(f"您的识别码为:\n{x}")
            return (x,)
        else:
            with open(Authorization_path, "w") as f:
                f.write(Verification)
        if check():
            return ("已授权",)
        else:
            return(f"校验失败，密码错误或已过期，请根据识别码\n{x}\n重新获取授权码",)
