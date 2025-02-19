from selenium import webdriver
import pickle
import os
from selenium.webdriver.support.ui import WebDriverWait

# 启动浏览器
driver = webdriver.Edge()

# 打开目标网站
driver.get('https://www.liblib.art')

# 等待一段时间以确保登录并生成 cookies
input("按任意键保存 cookies...")

# 获取 cookies
cookies = driver.get_cookies()

# 保存 cookies 到文件
cookies_path = "cookies.pkl"
with open(cookies_path, "wb") as f:
    pickle.dump(cookies, f)

# 打印 cookies 文件的绝对路径
absolute_path = os.path.abspath(cookies_path)
print(f"cookies 文件已保存至: {absolute_path}")

# 关闭浏览器
driver.quit()
