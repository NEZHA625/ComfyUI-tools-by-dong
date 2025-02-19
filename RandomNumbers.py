import os
import time
import random
import hashlib
from check import check
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
                "salt": ("STRING", {"default": ""}),  # 新增盐值输入
            }
        }

    RETURN_TYPES = ("BOOLEAN", "INT")  # 返回类型是布尔值
    RETURN_NAMES = ("bool", "num")  # 返回变量名是bool
    FUNCTION = "Random_numbers"  # 执行的入口方法
    CATEGORY = "dong_tools/Random_numbers_by_dong"  # 分类，决定显示在哪一类节点下

    def Random_numbers(self, numbers, digits, is_enable, salt=""):  
        if not check():
            print("未授权用户")
            return (False,)
        if not is_enable:
            print("功能已禁用")
            return (False,)  
        
        # 如果传入的是-1，则根据数字位数生成随机数
        if numbers == -1:
            # 使用盐值和当前时间戳来生成一个更复杂的种子
            random.seed(hashlib.sha256((salt + str(time.time())).encode('utf-8')).hexdigest())
            num = random.randint(10**(digits-1), 10**digits - 1)
            return (True, num)
        else:
            # 如果numbers不为-1，则直接返回该值
            num = numbers
            return (True, num)

    @classmethod
    def IS_CHANGED(cls, is_enable):
        return True
