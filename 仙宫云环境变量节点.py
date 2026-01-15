import os

class 仙宫云环境变量节点:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "变量": (["实例ID", "云存储路径", "UUID"], {"default": "实例ID"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("INFO",)
    FUNCTION = "run"
    CATEGORY = "dong_tools/get_xgy_environment_variables_by_dong"

    def run(self, 变量):
        # 对应映射
        env_map = {
            "实例ID": os.getenv("XGC_INSTANCE_ID", ""),
            "云存储路径": os.getenv("XGC_CLOUD_PATH", ""),
            "UUID": os.getenv("XGC_UUID", ""),
        }

        # 只返回单个变量对应的值
        info = env_map.get(变量, "")

        return (info,)
