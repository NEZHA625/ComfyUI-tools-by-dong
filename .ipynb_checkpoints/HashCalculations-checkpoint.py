import os
import hashlib

class HashCalculationsNode:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "file_absolute_path": ("STRING", {"default": "source_directory"}),  # 源路径
                "digits": ("INT", {"default": 12}), 
                "is_enable": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "is_change":("BOOLEAN",{"default":True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")  # 返回类型是布尔值和字符串（哈希值）
    RETURN_NAMES = ("bool", "hashes")  # 返回变量名是bool和hashes
    FUNCTION = "HashCalculations"  # 执行的入口方法
    CATEGORY = "dong_tools/Hash_Calculations_by_dong"  # 分类，决定显示在哪一类节点下

    def HashCalculations(self, file_absolute_path, digits, is_enable,is_change):
        
        if not is_enable:
            print("功能已禁用")
            return (False,)  # 如果禁用，则返回 False

        # 检查文件是否存在
        if not os.path.exists(file_absolute_path):
            print(f"错误：文件 {file_absolute_path} 不存在")
            return (False,)
        
        # 计算文件哈希值
        try:
            hash_md5 = hashlib.md5()  # 你可以根据需要选择不同的哈希算法，比如 sha256
            with open(file_absolute_path, "rb") as f:
                # 每次读取一定大小的数据来计算哈希，避免大文件占用过多内存
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            file_hash = hash_md5.hexdigest()
            
            # 截取前 digits 位
            truncated_hash = file_hash[:digits]
            return (True, truncated_hash)
        
        except Exception as e:
            print(f"哈希计算时发生错误: {e}")
            return (False,)

