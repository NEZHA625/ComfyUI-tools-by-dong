from selenium import webdriver
import pickle
import os
from selenium.webdriver.support.ui import WebDriverWait
import time
from check import check
# 获取 ComfyUI_path 路径
ComfyUI_tools_by_dong_path = os.path.dirname(os.path.abspath(__file__))
custom_node_path = os.path.dirname(ComfyUI_tools_by_dong_path)
ComfyUI_path = os.path.dirname(custom_node_path)

# 检查并创建 cookies 文件夹
cookies_folder = os.path.join(ComfyUI_path, "cookies")
if not os.path.exists(cookies_folder):
    os.makedirs(cookies_folder)

class Get_cookies_Node:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "platform": (["LibLib", "tusi", "runninghub", "kuaishou", "xhs", "douyin", "qq","dewu","shipinghao","civitai", "ins", "tiktok", "pinterest", "twitter"], {"default": "LibLib"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("bool",)
    FUNCTION = "Get_cookies"
    CATEGORY = "dong_tools/Get_cookies_by_dong"

    def Get_cookies(self, platform, is_enable):
        if not check():
            print("未授权用户")
            return (False,)
            
        if not is_enable:
            print("功能已禁用")
            return (False,)  # 如果禁用，则返回 False
        
        platform_url = {
            "LibLib": "https://www.liblib.art",
            "tusi": "http://tusiart.cn/",
            "runninghub": "https://www.runninghub.cn/",
            "kuaishou": "https://cp.kuaishou.com/article/publish/video?origin=www.kuaishou.com",
            "xhs": "https://creator.xiaohongshu.com/login?selfLogout=true",
            "douyin": "https://creator.douyin.com/",
            "qq": "https://qqzz.qq.com/",
            "dewu":"https://creator.dewu.com/release",
            "shipinghao":"https://channels.weixin.qq.com/login.html",
            "civitai": "https://civitai.com/login?returnUrl=/",
            "ins": "https://www.instagram.com/",
            "tiktok": "https://www.tiktok.com/",
            "pinterest": "https://www.pinterest.com/",
            "twitter": "https://x.com/",
        }

        # 确保选定的平台存在
        if platform not in platform_url:
            print(f"平台 {platform} 不支持")
            return (False,)

        # 启动浏览器
        driver = webdriver.Edge()

        try:
            # 打开目标网站
            driver.get(platform_url[platform])  # 使用动态平台网址

            # 等待一段时间以确保登录并生成 cookies
            input("按任意键保存 cookies...")

            # 获取 cookies
            cookies = driver.get_cookies()

            # 保存 cookies 到文件
            cookies_path = os.path.join(cookies_folder, f"{platform}_cookies.pkl")
            with open(cookies_path, "wb") as f:
                pickle.dump(cookies, f)

            # 打印 cookies 文件的绝对路径
            absolute_path = os.path.abspath(cookies_path)
            print(f"cookies 文件已保存至: {absolute_path}")

        finally:
            # 关闭浏览器
            driver.quit()

        return True

    @classmethod
    def IS_CHANGED(cls, platform, is_enable):
        return True
