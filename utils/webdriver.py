# utils/webdriver.py
# 一些和 WebDriver 相關的工具函式
# get_driver() - 根據 dev_config 的設定，創建並回傳一個配置好的 WebDriver 物件。

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from . import dev_config


def get_driver() -> webdriver.Chrome:
    """
    從 dev_config 中的 WEBDRIVER_CONFIG，創建並配置 Chrome WebDriver。

    Args:
        None

    Returns:
        webdriver.Chrome: 配置好的 WebDriver 實例
    """
    options = Options()
    cfg = dev_config.WEBDRIVER_CONFIG

    # WebDriver debug 模式 - 是否顯示瀏覽器視窗
    if not cfg.get("webdriver_debug", False):
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

    # 自定義 User-Agent
    if cfg.get("user_agent", None):
        options.add_argument(f"user-agent={cfg['user_agent']}")

    # 其他常用設定
    options.add_argument("--no-sandbox")  # 避免權限問題 (容器環境)
    options.add_argument("--disable-dev-shm-usage")  # 避免記憶體不足 (ai 提供)

    # 創建 driver
    driver = webdriver.Chrome(options=options)

    # 設定隱式等待（可選）
    driver.implicitly_wait(10)

    return driver
