from selenium.webdriver.common.by import By
from selenium import webdriver
import time


def login(
    driver: webdriver.Chrome,
    username: str,
    password: str,
    sleeping_time: int,
) -> None:
    """
    網站登入流程，需要提供學號與密碼，才可以正確運作。

    Args:
        driver (webdriver.Chrome): 已初始化的 Chrome WebDriver 實例
        username (str): 使用者學號
        password (str): 使用者密碼
    Returns:
        None
    """
    # 找學號輸入框
    driver.find_element(By.ID, "MainContent_TxtUSERNO").send_keys(username)

    # 找密碼輸入框
    driver.find_element(By.ID, "MainContent_TxtPWD").send_keys(password)

    # 找登入按鈕
    driver.find_element(By.ID, "MainContent_Button1").click()
    time.sleep(sleeping_time)

    # 開啟申請表單
    driver.find_element(By.ID, "MainContent_Button2").click()
