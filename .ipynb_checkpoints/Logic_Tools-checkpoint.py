class LogicToolsNode:
    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "A": ("BOOLEAN", {}),  # 第一个布尔值A
                "logic_type": (["and", "or"], {"default": "and"}),  # 逻辑类型
                "is_enable": ("BOOLEAN", {"default": False}),  # 启用状态
            },
            "optional": {
                "B": ("BOOLEAN", {"default": True}),  # 第二个布尔值B，默认True
                "C": ("BOOLEAN", {"default": True}),  # 第三个布尔值C，默认True
                "D": ("BOOLEAN", {"default": True}),  # 第四个布尔值D，默认True
            }
        }

    RETURN_TYPES = ("BOOLEAN",)  # 返回类型是布尔值
    RETURN_NAMES = ("bool",)  # 返回变量名是bool

    FUNCTION = "logictools"  # 执行的入口方法

    OUTPUT_NODE = True  # 是否是输出节点

    CATEGORY = "dong_tools/Logic_by_dong"  # 分类，决定显示在哪一类节点下

    def logictools(self, A, B, C, D, logic_type="and", is_enable=True):
        """
        执行逻辑运算，返回操作结果。
        """
        print(f"A为{A}, B为{B}, C为{C}, D为{D}, 逻辑类型: {logic_type}")

        if not is_enable:
            return (False,)  # 如果禁用，则返回 False

        if logic_type == "and":
            result = A and B and C and D
            print(f"AND operation result: {result}")  # 调试输出
            return (result,)
        elif logic_type == "or":
            result = A or B or C or D
            print(f"OR operation result: {result}")  # 调试输出
            return (result,)

    @classmethod
    def IS_CHANGED(cls, A, logic_type, is_enable, B, C, D):
        """
        检查输入值是否发生变化。
        """
        return True
        
