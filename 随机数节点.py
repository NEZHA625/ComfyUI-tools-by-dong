import os
import time
import random
import hashlib

class 随机数节点:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "数字": ("INT", {"default": -1}), 
                "位数": ("INT", {"default": 10}), 
                "盐值": ("STRING", {"default": "QQ917724495"}), 
            }
        }

    RETURN_TYPES = ("INT",)  
    RETURN_NAMES = ("数字",) 
    FUNCTION = "Random_numbers"  
    CATEGORY = "dong_tools/Random_numbers_by_dong"

    def Random_numbers(self, 数字, 位数, 盐值=""):  
        """
        如果传入的初始数字为 -1，则根据数字位数和盐值生成随机数；
        否则直接返回传入的初始数字。
        """
        if 数字 == -1:
            # 使用盐值和当前时间戳生成复杂随机种子
            random.seed(hashlib.sha256((盐值 + str(time.time())).encode('utf-8')).hexdigest())
            数字 = random.randint(10**(位数-1), 10**位数 - 1)
            return (True, 数字)
        else:
            # 如果初始数字不为 -1，则直接返回该值
            return (True, 数字)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return True
