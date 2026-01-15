class AlwaysEqualProxy(str):
    def __eq__(self, _):
        return True

    def __ne__(self, _):
        return False

any_type = AlwaysEqualProxy("*")

class 数据存在性检测节点:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "data": (any_type,), 
                "is_enable":("BOOLEAN",{"defalut":False}),
            }
        }
    
    RETURN_TYPES = ("BOOLEAN",any_type)  
    RETURN_NAMES = ("bool", "data")  
    FUNCTION = "detect_input"  
    CATEGORY = "dong_tools/Data_detect_by_dong"  

    def detect_input(self, data, is_enable):
        
        if not is_enable:
            return (False, "功能未启用")

        if data is not None:
            return (True, data)  # 数据不为空时，返回True和数据
        return (False, "error")  # 数据为空时，返回False和"error"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return True
