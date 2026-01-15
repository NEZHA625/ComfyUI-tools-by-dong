import json
import os
import re

class JSON取值节点:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "JSON路径或文本": ("STRING",),  # JSON文件路径或文本
                "键": ("STRING", {"default": "key"}),  # 查询的键
                "节点开关": ("BOOLEAN", {"default": True}),  # 是否启用节点
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")
    RETURN_NAMES = ("状态", "值")
    FUNCTION = "获取_json值"
    CATEGORY = "dong_tools/get_json_value_by_dong"

    def _递归查找(self, data, key):
        """
        递归搜索字典或列表，返回第一个匹配的 key 的值
        """
        if isinstance(data, dict):
            if key in data:
                return data[key]
            for v in data.values():
                res = self._递归查找(v, key)
                if res is not None:
                    return res
        elif isinstance(data, list):
            for item in data:
                res = self._递归查找(item, key)
                if res is not None:
                    return res
        return None

    def 获取_json值(self, JSON路径或文本, 键, 节点开关):
        if not 节点开关:
            print("功能已禁用")
            return (False, "")

        # 加载 JSON 数据
        if os.path.isfile(JSON路径或文本):
            if not JSON路径或文本.endswith('.json'):
                return (False, "传入的文件不是以.json结尾")
            try:
                with open(JSON路径或文本, 'r', encoding='utf-8') as f:
                    json数据 = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return (False, "JSON解析失败")
        else:
            # 字符串处理
            JSON路径或文本 = JSON路径或文本.strip()
            try:
                json数据 = json.loads(JSON路径或文本)
            except json.JSONDecodeError:
                # 尝试正则提取大括号内容
                pattern = r'\{.*\}'
                match = re.search(pattern, JSON路径或文本, re.DOTALL)
                if match:
                    try:
                        json数据 = json.loads(match.group(0))
                    except json.JSONDecodeError:
                        return (False, "JSON解析失败")
                else:
                    return (False, "无效的JSON文本")

        # 先尝试最外层直接键
        if 键 in json数据:
            值 = json数据[键]
        else:
            # 外层没有，再递归搜索内层
            值 = self._递归查找(json数据, 键)

        if 值 is not None:
            # 格式化输出
            格式化值 = json.dumps(值, ensure_ascii=False, indent=4)
            格式化值 = 格式化值.replace("\\n", "\n")
            if isinstance(值, str) and 格式化值.startswith('"') and 格式化值.endswith('"'):
                格式化值 = 格式化值[1:-1]
            return (True, 格式化值)
        else:
            return (False, f"键'{键}'不存在于JSON数据中")
