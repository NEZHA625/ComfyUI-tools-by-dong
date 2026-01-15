import json

class JSON单键值构建节点:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "键": ("STRING", {"default": "key"}),
                "值": ("STRING", {"default": "value"}),
            }
        }

    CATEGORY = "dong_tools/http_api_node_by_dong"
    FUNCTION = "json构建"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json",)

    def json构建(self, 键, 值):
        # 先处理布尔
        if isinstance(值, str):
            if 值.lower() == "true":
                值 = True
            elif 值.lower() == "false":
                值 = False
            else:
                # 尝试 int
                try:
                    值 = int(值)
                except ValueError:
                    # 尝试 float
                    try:
                        值 = float(值)
                    except ValueError:
                        pass  # 保持原来的字符串
        data = {键: 值}
        json_body = json.dumps(data, ensure_ascii=False)
        return (json_body,)