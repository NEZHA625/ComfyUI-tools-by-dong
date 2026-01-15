import json

class JSON合并节点:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json1": ("STRING", {"default": "{}"}),
                "json2": ("STRING", {"default": "{}"}),
            }
        }

    CATEGORY = "dong_tools/json_utils"
    FUNCTION = "JSON合并"
    RETURN_TYPES = ("BOOLEAN", "STRING")
    RETURN_NAMES = ("state", "json")

    def JSON合并(self, json1, json2):
        """
        将两个 JSON 字符串合并为一个 JSON 字符串
        如果存在相同 key，则返回 False 并提示
        """
        try:
            dict1 = json.loads(json1) if json1.strip() else {}
            dict2 = json.loads(json2) if json2.strip() else {}

            if not isinstance(dict1, dict) or not isinstance(dict2, dict):
                return (False, "输入必须是 JSON 对象")

            # 检查重复 key
            duplicate_keys = set(dict1.keys()) & set(dict2.keys())
            if duplicate_keys:
                return (False, f"检测到重复 key: {', '.join(duplicate_keys)}")

            # 合并 dict1 和 dict2
            merged = {**dict1, **dict2}
            return (True, json.dumps(merged, ensure_ascii=False))
        except Exception as e:
            return (False, f"JSON 合并错误: {str(e)}")
