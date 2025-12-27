import os
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from check import check


class liblib_auto_video_node:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_list": ("STRING", {"multiline": True, "default": ""}),
                "resolution": (["720P", "1080P"], {"default": "1080P"}),
                "aspect_ratio": (["16:9", "9:16", "1:1", "4:3", "3:4"], {"default": "9:16"}),
                "audio": ([True, False], {"default": True}),
                "duration": (["5s", "10s", "15s"], {"default": "15s"}),
                "time_sleep": ("INT", {"default": 5, "min": 1, "max": 60}),
                "is_enable": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")
    RETURN_NAMES = ("success", "log")
    FUNCTION = "liblib_auto_video"
    CATEGORY = "dong_tools/liblib_video"

    def liblib_auto_video(
        self,
        prompt_list,
        resolution,
        aspect_ratio,
        audio,
        duration,
        time_sleep,
        is_enable
    ):
        # ---- 路径处理 ----
        node_path = os.path.dirname(os.path.abspath(__file__))
        comfyui_path = os.path.dirname(os.path.dirname(node_path))
        cookies_file = os.path.join(comfyui_path, "cookies", "liblib_cookies.pkl")

        if not os.path.exists(cookies_file):
            return False, "cookies 不存在，请先登录并保存"

        if not check():
            return False, "未授权用户"

        if not is_enable:
            return False, "功能已禁用"

        prompts = [p.strip() for p in prompt_list.split("\n") if p.strip()]
        if not prompts:
            return False, "prompt 为空"

        log_lines = []

        # ---- 启动浏览器 ----
        options = webdriver.EdgeOptions()
        options.add_experimental_option("detach", True)  # 浏览器关闭不退出
        driver = webdriver.Edge(options=options)
        wait = WebDriverWait(driver, 25)

        try:
            driver.get("https://www.liblib.art")
            time.sleep(2)

            # ---- 加载 cookies ----
            with open(cookies_file, "rb") as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    driver.add_cookie(cookie)
            driver.refresh()
            print("[LOG] Cookies 已加载并刷新页面")
            time.sleep(time_sleep)

            # ---- 进入视频生成页面 ----
            driver.get("https://www.liblib.art/ai-tool/video-generator?modelid=22222563")
            print("[LOG] 已进入视频生成页面")
            time.sleep(5)
            
            # ---- 点击参数控制面板图标 ----
            try:
                icon_btn = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//i[contains(@class,'liblibfont') and contains(@class,'icon-procustom')]")
                ))
                driver.execute_script("arguments[0].scrollIntoView(true);", icon_btn)
                driver.execute_script("arguments[0].click();", icon_btn)
                print("[LOG] 已点击参数控制面板图标")
            except TimeoutException:
                return False, "未找到参数控制面板图标"
            except Exception as e:
                return False, f"点击参数控制面板图标异常: {e}"

            # ---- 设置分辨率 ----
            res_el = wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//div[contains(@class,'cursor-pointer') and contains(text(),'{resolution}')]")
            ))
            driver.execute_script("arguments[0].scrollIntoView(true);", res_el)
            driver.execute_script("arguments[0].click();", res_el)
            print(f"[LOG] 设置分辨率: {resolution}")

            # ---- 设置画幅比例 ----
            ar_el = wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//div[span[text()='{aspect_ratio}']]")
            ))
            driver.execute_script("arguments[0].scrollIntoView(true);", ar_el)
            driver.execute_script("arguments[0].click();", ar_el)
            print(f"[LOG] 设置画幅比例: {aspect_ratio}")

            # ---- 设置音频 ----
            if audio:
                audio_el = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(text(),'开启')]")
                ))
            else:
                audio_el = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(text(),'关闭')]")
                ))
            driver.execute_script("arguments[0].click();", audio_el)
            print(f"[LOG] 设置音频: {'开启' if audio else '关闭'}")

            # ---- 设置时长 ----
            dur_el = wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//div[text()='{duration}']")
            ))
            driver.execute_script("arguments[0].scrollIntoView(true);", dur_el)
            driver.execute_script("arguments[0].click();", dur_el)
            print(f"[LOG] 设置时长: {duration}")

            # ---- 关闭参数控制面板 ----
            time.sleep(1)
            driver.execute_script("document.body.click();")
            print("[LOG] 参数控制面板已关闭")

            # ---- 循环提交 prompt ----
            for idx, prompt in enumerate(prompts, start=1):
                textarea = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea")))
                try:
                    textarea.click()
                except:
                    driver.execute_script("arguments[0].click();", textarea)
                    print("[LOG] textarea 被遮挡，用 JS 点击")
                textarea.send_keys(Keys.CONTROL, "a")
                textarea.send_keys(Keys.BACKSPACE)
                textarea.send_keys(prompt)
                print(f"[LOG] 第 {idx} 条 prompt 输入完成: {prompt}")
                time.sleep(time_sleep)

                gen_btn = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//button[contains(.,'免积分') or contains(.,'生成') or contains(.,'0')]")
                ))
                driver.execute_script("arguments[0].click();", gen_btn)
                print(f"[LOG] 第 {idx} 条 prompt 已点击生成按钮")

                log_lines.append(f"第 {idx} 条 prompt 已提交 | 分辨率:{resolution} | 画幅:{aspect_ratio} | 时长:{duration} | 音频:{audio}")
                time.sleep(1)

        except TimeoutException as e:
            return False, f"页面元素加载超时: {e}"
        except Exception as e:
            return False, f"运行异常: {e}"
        finally:
            # 浏览器保持打开，不关闭
            pass

        for line in log_lines:
            print(f"[LOG] {line}")

        return True, "\n".join(log_lines)
