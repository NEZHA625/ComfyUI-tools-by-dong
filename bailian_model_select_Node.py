class bailian_model_select_Node:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_name": (
                    ["wanx2.1-t2v-turbo", "wanx2.1-t2v-plus", "wanx2.1-i2v-turbo", "wanx2.1-i2v-plus", "wanx2.1-kf2v-plus"],
                    {"default": "wanx2.1-t2v-turbo"}
                )
            }
        }

    RETURN_TYPES = ("STRING",)  
    RETURN_NAMES = ("model",) 
    FUNCTION = "modelchose" 
    CATEGORY = "dong_tools/bailian_model_select_by_dong" 

    def modelchose(self, model_name):
        return (model_name,)
