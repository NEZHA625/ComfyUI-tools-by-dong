import json

class JSON多键值构建节点:
    MAX_DYNAMIC_PORTS = 10  # 支持最多10个 key/value 对，可按需要改

    @classmethod
    def INPUT_TYPES(cls):
        # 动态生成 key/value 输入口，命名为 key1, value1, key2, value2 ...
        optional_ports = {}
        for i in range(1, cls.MAX_DYNAMIC_PORTS + 1):
            optional_ports[f"key{i}"] = ("STRING",)
            optional_ports[f"value{i}"] = ("STRING",)
        return {
            "optional": optional_ports
        }

    CATEGORY = "dong_tools/http_api_node_by_dong"
    FUNCTION = "json构建"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json",)

    def _类型转换(self, 值):
        """根据字符串内容自动转换为 bool / int / float / str"""
        if isinstance(值, str):
            low = 值.lower()
            if low == "true":
                return True
            elif low == "false":
                return False
            else:
                try:
                    f = float(值)
                    if f.is_integer():
                        return int(f)
                    return f
                except ValueError:
                    return 值
        return 值

    def json构建(self, **kwargs):
        """
        kwargs 中包含 key1, value1, key2, value2 ...
        会把非空的 key/value 组合成 JSON，自动类型转换
        空值或 None 会被跳过
        """
        data = {}
        # 按顺序处理 key/value 对
        for i in range(1, self.MAX_DYNAMIC_PORTS + 1):
            key = kwargs.get(f"key{i}")
            value = kwargs.get(f"value{i}")
            if key and value not in (None, ""):  # key 不空且 value 有实际内容才加入
                data[key] = self._类型转换(value)
        json_body = json.dumps(data, ensure_ascii=False)
        return (json_body,)
