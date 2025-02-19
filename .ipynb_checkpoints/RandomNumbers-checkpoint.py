import os
import time
import random

class RandomNumbersNode:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "numbers": ("INT", {"default": -1}), 
                "digits": ("INT", {"default": 10}), 
                "is_enable": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "INT")  # 返回类型是布尔值
    RETURN_NAMES = ("bool", "num")  # 返回变量名是bool
    FUNCTION = "Random_numbers"  # 执行的入口方法
    CATEGORY = "dong_tools/Random_numbers_by_dong"  # 分类，决定显示在哪一类节点下

    def Random_numbers(self, numbers, digits, is_enable):     
        if not is_enable:
            print("功能已禁用")
            return (False,)  
        if numbers == -1:
            # 产生digits位数的随机数
            num = random.randint(10**(digits-1), 10**digits - 1)
            return (True, num)
        else:
            num = numbers
            return (True, num)

    @classmethod
    def IS_CHANGED(cls, is_enable):
        return True