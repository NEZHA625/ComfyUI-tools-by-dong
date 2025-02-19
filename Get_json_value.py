import json
import os
import re
from check import check
class Get_json_value_Node:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "json_text_or_path": ("STRING", {"default": "json"}),  # 源路径或JSON文本
                "key":("STRING", {"default": "key"}),  # 键值
                "is_enable": ("BOOLEAN", {"default": True}),  # 是否启用功能
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")  # 返回类型是布尔值与字符串
    RETURN_NAMES = ("bool", "value")  # 返回变量名是bool和value
    FUNCTION = "get_json_value"  # 执行的入口方法
    CATEGORY = "dong_tools/get_json_value_by_dong"  # 分类，决定显示在哪一类节点下

    def get_json_value(self, json_text_or_path, key, is_enable):
        if not check():
            print("未授权用户")
            return (False,)
            
        if not is_enable:
            print("功能已禁用")
            return (False,)  # 如果禁用，则返回 False

        # 判断json_text_or_path是json文件路径还是字符串
        if os.path.isfile(json_text_or_path):
            # 如果是文件路径
            if not json_text_or_path.endswith('.json'):
                return (False, "传入的文件不是以.json结尾")
            
            # 检查文件是否存在
            try:
                with open(json_text_or_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
            except FileNotFoundError:
                return (False, "文件未找到")
            except json.JSONDecodeError:
                return (False, "文件内容不是有效的JSON格式")
            
            # 根据key取得对应的值
            if key in json_data:
                # 格式化输出并将 \n 转换为换行符
                formatted_value = json.dumps(json_data[key], ensure_ascii=False, indent=4)
                formatted_value = formatted_value.replace("\\n", "\n")
                if formatted_value.startswith('"') and formatted_value.endswith('"'):
                    formatted_value = formatted_value[1:-1]
                return (True, formatted_value)  # 将 \n 替换为换行符
            else:
                return (False, f"键'{key}'不存在于JSON数据中")
        
        else:
            # 如果是字符串
            json_text_or_path = json_text_or_path.strip()

            # 使用正则表达式检查字符串是否为有效的JSON格式
            try:
                # 尝试直接解析
                json_data = json.loads(json_text_or_path)
            except json.JSONDecodeError:
                # 使用正则提取大括号内的内容
                pattern = r'\{.*\}'
                match = re.search(pattern, json_text_or_path, re.DOTALL)
                if match:
                    # 提取到的大括号内内容
                    json_text_or_path = match.group(0)
                    try:
                        # 尝试解析提取的JSON
                        json_data = json.loads(json_text_or_path)
                    except json.JSONDecodeError:
                        return (False, "传入的文本格式错误，无法解析为JSON")
                else:
                    return (False, "传入的文本既不是有效的JSON格式，也无法深度解析为JSON")

            # 根据key取得对应的值
            if key in json_data:
                formatted_value = json.dumps(json_data[key], ensure_ascii=False, indent=4)
                formatted_value = formatted_value.replace("\\n", "\n")
                if formatted_value.startswith('"') and formatted_value.endswith('"'):
                    formatted_value = formatted_value[1:-1]
                return (True, formatted_value)  # 将 \n 替换为换行符
            else:
                return (False, f"键'{key}'不存在于JSON数据中")
