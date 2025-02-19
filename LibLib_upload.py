from selenium import webdriver
import pickle
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from check import check
class LibLib_upload_Node:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回节点输入参数的配置。
        """
        return {
            "required": {
                "model_name": ("STRING", {"default": "model_name"}), 
                "version_name": ("STRING", {"default": "1.0"}), 
                "description": ("STRING", {"default": "description"}), 
                "file_path": ("STRING", {"default": "model_file_path"}), 
                "loraDes": ("STRING", {"default": "美女"}), 
                "cookies_file": ("STRING", {"default": "cookies_file_path"}), 
                "images_path": ("STRING", {"default": "images_path"}), 
                "mode":(["sd15","sdxl","flux"], {"default": "flux"}),
                "timeout_upload_lora": ("INT", {"default": 300}),
                "timeout_upload_images": ("INT", {"default": 15}),
                "time_sleep": ("INT", {"default": 3}),
                "allow_download": ("BOOLEAN", {"default": True}),
                "allow_vip_download": ("BOOLEAN", {"default": False}),
                "allow_encrypt": ("BOOLEAN", {"default": False}),
                "allow_exclusive": ("BOOLEAN", {"default": False}),
                "is_enable": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("BOOLEAN","STRING")  # 返回类型是布尔值
    RETURN_NAMES = ("bool","log")  # 返回变量名是bool
    FUNCTION = "upload_to_liblib"  # 执行的入口方法
    CATEGORY = "dong_tools/upload_to_liblib_by_dong"  # 分类，决定显示在哪一类节点下

    def upload_to_liblib(self, model_name,version_name,description, file_path,loraDes,cookies_file,images_path,mode,timeout_upload_lora,timeout_upload_images,time_sleep,allow_download,allow_vip_download,allow_encrypt,allow_exclusive,is_enable):
        
        time.sleep(time_sleep)  # 模拟延迟
        if not check():
            print("未授权用户")
            return (False,)
        if not is_enable:
            print("功能已禁用")
            return (False,)  # 如果禁用，则返回 False

        # 检查文件是否存在
        if not os.path.exists(cookies_file):
            print("错误：cookies不存在")
            return (False,)
        
        # 启动浏览器
        driver = webdriver.Edge()
        
        # 打开目标网站
        driver.get('https://www.liblib.art')
        
        # 加载保存的 cookies
        try:
            with open(cookies_file, "rb") as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    driver.add_cookie(cookie)
            print("Cookies 加载成功")
        except Exception as e:
            print(f"加载 cookies 时出错: {e}")
        
        # 刷新页面，应用 cookies
        driver.refresh()
        time.sleep(time_sleep)
        
        # 打开模型上传页面
        driver.get('https://www.liblib.art/uploadmodel')
        time.sleep(time_sleep)
        
        # 1. 输入模型名字
        model_name_space = driver.find_element(By.ID, 'name')
        model_name_space.send_keys(model_name)
        
        # 2. 输入模型类型
        def select_model_type(driver):
            try:
                # 等待并定位到选择框并点击，展示下拉菜单
                selector = WebDriverWait(driver, time_sleep).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-select-selector']"))
                )
                selector.click()
                # 等待并选择 "LoRA" 选项
                loRA_option = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@title='LoRA']"))
                )
                loRA_option.click()
                print("成功选择 LoRA 模型类型")
            except Exception as e:
                print(f"选择模型类型时出错: {e}")
        select_model_type(driver)
        
        # 3. 点击下一步
        next_button = WebDriverWait(driver, time_sleep).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='下一步']"))
        )
        next_button.click()
        time.sleep(time_sleep)
        
        # 4. 输入版本名称
        version_input = WebDriverWait(driver, time_sleep).until(
            EC.presence_of_element_located((By.ID, 'versions_0_name'))
        )
        version_input.send_keys(version_name)
        time.sleep(time_sleep)
        
        # 5. 输入基础模型算法
        if mode == "flux":
            placeholder = WebDriverWait(driver, time_sleep).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'ant-select-selection-placeholder'))
            )
            actions = ActionChains(driver)
            actions.move_to_element(placeholder).click().perform()
            basemodel_option = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-select-item-option-content' and text()='基础算法 F.1']"))
            )
            actions.move_to_element(basemodel_option).click().perform()
            time.sleep(time_sleep)
        elif mode == "sd15":
            placeholder = WebDriverWait(driver, time_sleep).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'ant-select-selection-placeholder'))
            )
            actions = ActionChains(driver)
            actions.move_to_element(placeholder).click().perform()
            basemodel_option = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-select-item-option-content' and text()='基础算法 v1.5']"))
            )
            actions.move_to_element(basemodel_option).click().perform()
            time.sleep(time_sleep)
        else:
            placeholder = WebDriverWait(driver, time_sleep).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'ant-select-selection-placeholder'))
            )
            actions = ActionChains(driver)
            actions.move_to_element(placeholder).click().perform()
            basemodel_option = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-select-item-option-content' and text()='基础算法 XL']"))
            )
            actions.move_to_element(basemodel_option).click().perform()
            time.sleep(time_sleep)

        # 6. 输入版本介绍
        description_space = driver.find_element(By.ID, 'w-e-element-0')
        description_space.send_keys(description)
        time.sleep(time_sleep)
        
        # 7. 点击此版本不需要任何触发词
        TriggerWord_space = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='versions_0_noTriggerWord']"))
        )
        TriggerWord_space.click()
        time.sleep(1)
        
        # 8. 输入模型描述
        loraDes_space = driver.find_element(By.ID, 'versions_0_loraDes')
        loraDes_space.send_keys(loraDes)
        time.sleep(time_sleep)
        
        # 9. 选择推荐Checkpoint
        if mode == "flux":
            input_element = driver.find_element(By.ID, "versions_0_ckpt")
            input_element.send_keys("基础算法_F.1.safetensors")
            input_element.send_keys(Keys.RETURN)
            time.sleep(time_sleep)
        elif mode == "sd15":
            input_element = driver.find_element(By.ID, "versions_0_ckpt")
            input_element.send_keys("majicMIX realistic 麦橘写实_v7.safetensors")
            input_element.send_keys(Keys.RETURN)
            time.sleep(time_sleep)
        else:
            input_element = driver.find_element(By.ID, "versions_0_ckpt")
            input_element.send_keys("基础算法_XL.safetensors")
            input_element.send_keys(Keys.RETURN)
            time.sleep(time_sleep)           
        
        # 10. 点击此版本不需要任何高清修复
        HdSamplerMethods_space = driver.find_element(By.ID, 'versions_0_noHdSamplerMethods')
        HdSamplerMethods_space.click()
        time.sleep(1)

        # 11. 点击会员下载
        if allow_vip_download:
            try:
                # 使用 class 和 title 定位元素
                element = WebDriverWait(driver, time_sleep).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-segmented-item-label" and @title="会员下载"]'))
                )
                element.click()
                print("会员下载已启用")
            except TimeoutException:
                print("未能找到 会员下载 元素，超时")
        else:
            pass
        
        # 12. 点击独家模型
        if allow_exclusive:
            try:
                # 使用 id 定位元素
                checkbox = WebDriverWait(driver, time_sleep).until(
                    EC.element_to_be_clickable((By.ID, "versions_0_exclusive"))
                )
                # 点击复选框，模拟选中操作
                checkbox.click()
                print("勾选独家模型成功")
            except TimeoutException:
                print("未能找到独家模型元素，超时")
        else:
            pass

        # 13. 点击允许下载生图
        if allow_vip_download:
            pass
        else:
            if allow_download:
                openAccess_space = driver.find_element(By.ID, 'versions_0_openAccess')
                openAccess_space.click()
                time.sleep(1)
            else:
                pass
        
        # 14. 上传文件
        def upload_file(file_path):
            try:
                file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                file_input.send_keys(file_path)
                WebDriverWait(driver, timeout_upload_lora).until(
                    EC.text_to_be_present_in_element((By.XPATH, "//span[text()='100%']"), '100%')
                )
                print("文件上传成功")
                return True
            except TimeoutException:
                print("文件上传超时")
                return False
        time.sleep(time_sleep)

        # 15. 点击加密
        if allow_encrypt:
            # 等待并找到目标 span 元素
            try:
                # 使用 XPath 定位具有 "加密" 文本的 span 元素
                span_element = WebDriverWait(driver, time_sleep).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[text()="加密"]'))
                )
                # 点击该元素
                span_element.click()
                print("点击 '加密' 成功")
            except TimeoutException:
                print("未能找到 '加密' 元素，超时")
        else:
            pass

        # 16. 点击下一步
        if upload_file(file_path):
            next_button = WebDriverWait(driver, time_sleep).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., '下一步')]"))
            )
            next_button.click()
        else:
            print("点击下一步失败，上传失败，无法继续")
        time.sleep(time_sleep)
        
        # 17.上传图片
        image_files = []
        for file_name in os.listdir(images_path):
            file_path = os.path.join(images_path, file_name)
            if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_files.append(file_path)
        if not image_files:
            print("指定文件夹中没有图片文件")
            return (False, "指定文件夹中没有图片文件")  # 返回一个失败的状态

        image_count = (len(image_files))
        try:
            file_input = WebDriverWait(driver, time_sleep).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )  
            # 将所有图片路径合并成一个字符串，以空格分隔
            all_images_paths = '\n'.join(image_files)
            # 发送所有图片路径
            file_input.send_keys(all_images_paths)
        except TimeoutException:
            print("文件上传输入框未找到，上传失败")
        # 等待上传完成
        time.sleep(timeout_upload_images)
        
        # 18.点击 '发布' 按钮
        publish_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='mantine-UnstyledButton-root mantine-Button-root mantine-1t1awu']//span[text()='发布']"))
        )
        publish_button.click()
        print("点击 '发布' 按钮成功")
        time.sleep(time_sleep)
        # 16.关闭浏览器
        print(f"成功发布{model_name}共{image_count}张图片")
        # input("按 Enter 键退出并关闭浏览器...")
        
        driver.quit()

    @classmethod
    def IS_CHANGED(cls,is_enable):
        return True