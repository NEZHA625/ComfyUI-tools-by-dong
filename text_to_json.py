import os
import json
from check import check
class TextToJsonNode:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "key_1": ("STRING", {"default": "key_1"}), 
                "value_1": ("STRING", {"default": "value_1"}),  
                "file_name": ("STRING", {"default": "file_name"}),
                "save_path": ("STRING", {"default": "save_path"}),
                "is_enable": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "key_2": ("STRING",), 
                "value_2": ("STRING",),    
                "key_3": ("STRING",), 
                "value_3": ("STRING",),  
                "key_4": ("STRING",), 
                "value_4": ("STRING",),    
                "key_5": ("STRING",), 
                "value_5": ("STRING",),  
                "key_6": ("STRING",), 
                "value_6": ("STRING",),    
                "key_7": ("STRING",), 
                "value_7": ("STRING",),  
                "key_8": ("STRING",), 
                "value_8": ("STRING",),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")  # 返回类型是布尔值
    RETURN_NAMES = ("bool", "json_path")  # 返回变量名是bool
    FUNCTION = "save_to_json"  # 执行的入口方法
    CATEGORY = "dong_tools/save_to_json_by_dong"  # 分类，决定显示在哪一类节点下

    def save_to_json(self, key_1, value_1, file_name, save_path, is_enable, 
                     key_2=None, value_2=None, key_3=None, value_3=None,
                     key_4=None, value_4=None, key_5=None, value_5=None,
                     key_6=None, value_6=None, key_7=None, value_7=None,
                     key_8=None, value_8=None):
        if not check():
            print("未授权用户")
            return (False,)
        if not is_enable:
            print("功能已禁用")
            return (False,)  # 如果禁用，则返回 False
        
        _, ext = os.path.splitext(file_name)
        if ext.lower() != '.json':
            file_name = file_name + '.json'
            
        json_path = os.path.join(save_path, file_name)

        if os.path.exists(json_path):
            print(f"错误：文件 {json_path} 已存在")
            return (False,)

        # 按照键值对构建一个字典
        data = {key_1: value_1}

        # 添加可选的键值对
        optional_keys = [("key_2", "value_2"), ("key_3", "value_3"), 
                         ("key_4", "value_4"), ("key_5", "value_5"),
                         ("key_6", "value_6"), ("key_7", "value_7"),
                         ("key_8", "value_8")]
        
        for key, value in optional_keys:
            key_value = locals().get(key)
            value_value = locals().get(value)
            if key_value and value_value:
                data[key_value] = value_value

        try:
            # 将字典转换为JSON并保存到文件
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"文件已保存至 {json_path}")
            return (True, json_path)
        except Exception as e:
            print(f"保存文件失败: {e}")
            return (False,)
