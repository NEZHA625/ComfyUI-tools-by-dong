import math

class 取整函数节点:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "整数": ("INT", {"default": None}),
                "浮点": ("FLOAT", {"default": None}),
                "模式": (["向上取整", "向下取整", "四舍五入", "截断小数"],),
            }
        }

    CATEGORY = "dong_tools/rounding_function_by_dong"
    FUNCTION = "取整函数"
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("结果",)

    def 取整函数(self, 整数=None, 浮点=None, 模式="向下取整"):
        # 自动选择输入：浮点优先，其次整数
        if 浮点 not in (None, 0.0):
            value = 浮点
        elif 整数 not in (None, 0):
            value = 整数
        else:
            return (0,)

        if 模式 == "向上取整":
            result = math.ceil(value)
        elif 模式 == "四舍五入":
            result = math.floor(value + 0.5) if value >= 0 else math.ceil(value - 0.5)
        elif 模式 == "截断小数":
            result = int(value)
        else:  # 向下取整
            result = math.floor(value)

        return (int(result),)
