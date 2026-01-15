class 逻辑节点:
    LETTERS = [chr(i) for i in range(ord("A"), ord("B") + 1)]  # A~Z

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                **{letter: ("BOOLEAN",) for letter in cls.LETTERS},
                "mode": (["and", "or", "not"], "default:and"),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("bool",)
    FUNCTION = "logictools"
    CATEGORY = "dong_tools/Logic_by_dong"

    def logictools(self, mode="and", **kwargs):
        # 收集实际布尔输入
        inputs = [v for k, v in sorted(kwargs.items()) if k in self.LETTERS and isinstance(v, bool)]

        if not inputs:
            return (False,)

        if mode == "and":
            result = all(inputs)
        elif mode == "or":
            result = any(inputs)
        elif mode == "not":
            # 只取第一个端口的反值
            result = not inputs[0]
        else:
            result = False

        return (result,)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return True
