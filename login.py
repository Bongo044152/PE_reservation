from selenium.webdriver.common.by import By
import time

def login(driver,username,password):
    # 找學號輸入框
    username_input = driver.find_element(By.ID, "MainContent_TxtUSERNO")
    username_input.send_keys(username)
    
    # 找密碼輸入框
    password_input = driver.find_element(By.ID, "MainContent_TxtPWD")
    password_input.send_keys(password)

    # 找登入按鈕
    login_button = driver.find_element(By.ID, "MainContent_Button1")
    login_button.click()
    time.sleep(3)
    
    login_button2 = driver.find_element(By.ID, "MainContent_Button2")
    login_button2.click()
    