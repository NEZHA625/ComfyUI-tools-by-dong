from check import check

class LogicToolsNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "A": ("BOOLEAN",), 
                "logic_type": (["and", "or"],),  
                "is_enable": ("BOOLEAN",), 
            },
            "optional": {
                "B": ("BOOLEAN",),  
                "C": ("BOOLEAN",),  
                "D": ("BOOLEAN",), 
                "E": ("BOOLEAN",),  
                "F": ("BOOLEAN",), 
                "G": ("BOOLEAN",),  
                "H": ("BOOLEAN",), 
            }
        }

    RETURN_TYPES = ("BOOLEAN",) 
    RETURN_NAMES = ("bool",)  
    FUNCTION = "logictools"  
    CATEGORY = "dong_tools/Logic_by_dong"  

    def logictools(self, A, logic_type="and", B=None, C=None, D=None, E=None, F=None, G=None, H=None,  is_enable=False):
        
        if not check():
            print("未授权用户")
            return (False,)

        if not is_enable:
            print("功能已禁用")
            return (False,) 

        # 收集所有有效的布尔值，不参与运算的项不加入列表
        values = [A]
        for var in [B, C, D, E, F, G, H]:
            if var is not None:
                values.append(var)
        
        # 根据逻辑类型执行运算
        if logic_type == "and":
            result = all(values)  # 检查所有有效布尔值是否都为True
            print(f"A为{A}, B为{B}, C为{C}, D为{D}, E为{E}, F为{F}, G为{G}, H为{H}, 逻辑类型: {logic_type}")
            print(f"AND operation result: {result}")  
            return (result,)
        elif logic_type == "or":
            result = any(values)  # 检查有效布尔值是否有一个为True
            print(f"A为{A}, B为{B}, C为{C}, D为{D}, E为{E}, F为{F}, G为{G}, H为{H}, 逻辑类型: {logic_type}")
            print(f"OR operation result: {result}") 
            return (result,)

    @classmethod
    def IS_CHANGED(cls, A, logic_type="and", B=None, C=None, D=None, E=None, F=None, G=None, H=None,  is_enable=False):
        return True
