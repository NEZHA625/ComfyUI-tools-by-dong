import os
from check import check

class CountFilesFromFolderNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "floder": ("STRING",),  
                "filetype": (["image","video","text","other"], {"default": "image"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN","INT")  
    RETURN_NAMES = ("bool","count") 
    FUNCTION = "CountFilesFromFolder" 
    CATEGORY = "dong_tools/CountFilesFromFolder_by_dong" 

    def CountFilesFromFolder(self, floder, filetype, is_enable):
        if not is_enable:
            print("功能已禁用")
            return (False, 0)

        if not check():
            print("未授权用户")
            return (False, 0)

        # Define file extensions for each type
        file_extensions = {
            "image": ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'],
            "video": ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv'],
            "text": ['.txt', '.docx', '.doc', '.pdf', '.rtf', '.md']
        }

        count = 0
        
        try:
            if not os.path.isdir(floder):
                print(f"文件夹不存在: {floder}")
                return (False, 0)

            for filename in os.listdir(floder):
                filepath = os.path.join(floder, filename)
                if os.path.isfile(filepath):
                    _, ext = os.path.splitext(filename)
                    ext = ext.lower()
                    
                    if filetype == "other":
                        # Check if the file doesn't belong to any known category
                        is_known_type = False
                        for extensions in file_extensions.values():
                            if ext in extensions:
                                is_known_type = True
                                break
                        if not is_known_type:
                            count += 1
                    elif filetype in file_extensions and ext in file_extensions[filetype]:
                        count += 1

            return (True, count)
            
        except Exception as e:
            print(f"计算文件数量时出错: {e}")
            return (False, 0)