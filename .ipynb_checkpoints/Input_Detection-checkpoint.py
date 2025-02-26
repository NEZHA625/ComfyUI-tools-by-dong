class InputDetectionNode:

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "data": ("*", {"default": None}),  # 任意类型的输入数据，默认为None
            }
        }
    
    RETURN_TYPES = ("BOOLEAN", "*")  # 返回类型是布尔值和任意类型的数据
    RETURN_NAMES = ("bool", "data")  # 返回变量名是bool和data
    FUNCTION = "detect_input"  # 执行的入口方法
    CATEGORY = "dong_tools/Input_Detection_by_dong"  # 分类，决定显示在哪一类节点下

    def detect_input(self, data):
        """
        检测输入的数据是否为None。如果不为None，返回True和数据本身。
        否则，返回False和"error"字符串。
        """
        if data is not None:
            return (True, data)  # 数据不为空时，返回True和数据
        return (False, "error")  # 数据为空时，返回False和"error"

    @classmethod
    def IS_CHANGED(s):
        return True
