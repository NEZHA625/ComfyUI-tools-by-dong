import re

class 字符处理节点:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文本": ("STRING",),
                "操作": (
                    [
                        "不改变",
                        "取数字",
                        "取字母",
                        "转大写",
                        "转小写",
                        "取中文",
                        "去标点",
                        "去换行",
                        "去空行",
                        "去空格",
                        "去格式",
                        "统计字数",
                        "清空",
                    ],
                    {"default": "不改变"},
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("文本",)
    FUNCTION = "字符处理"
    CATEGORY = "dong_tools/string_handle_by_dong"

    def is_chinese(self, char):
        return '\u4e00' <= char <= '\u9fff'

    def 字符处理(self, 文本, 操作):
        input_string = 文本

        if 操作 == "取数字":
            result = ''.join(re.findall(r'\d', input_string))

        elif 操作 == "取字母":
            result = ''.join(
                c for c in input_string if c.isalpha() and not self.is_chinese(c)
            )

        elif 操作 == "转大写":
            result = input_string.upper()

        elif 操作 == "转小写":
            result = input_string.lower()

        elif 操作 == "取中文":
            result = ''.join(c for c in input_string if self.is_chinese(c))

        elif 操作 == "去标点":
            result = re.sub(r'[^\w\s\u4e00-\u9fff]', '', input_string)

        elif 操作 == "去换行":
            result = input_string.replace('\n', '').replace('\r', '')

        elif 操作 == "去空行":
            result = '\n'.join(
                line for line in input_string.splitlines() if line.strip()
            )

        elif 操作 == "去空格":
            result = input_string.replace(' ', '')

        elif 操作 == "去格式":
            result = re.sub(r'\s+', '', input_string)

        elif 操作 == "统计字数":
            result = str(len(input_string))

        elif 操作 == "清空":
            result = ""

        else:  
            result = input_string

        return (result,)
