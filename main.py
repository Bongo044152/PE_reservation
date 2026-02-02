import datetime
import time
import traceback
import pytz
from selenium import webdriver
from login import login
import account
from form import fill_form
from robot import send_to_discord

def get_taiwan_time():
    tw_tz = pytz.timezone('Asia/Taipei')
    return datetime.datetime.now(tw_tz)

def run_reservation(target_date):
    driver = webdriver.Chrome()
    try:
        # 1. 前往登入
        driver.get("https://sys.ndhu.edu.tw/gc/sportcenter/SportsFields/Login.aspx")
        time.sleep(3)
        login(driver, account.account, account.password)
        time.sleep(3)

        # 2. 週日檢查邏輯 (免紀錄檔)
        now = get_taiwan_time()
        if now.weekday() == 6:  # 6 是週日
            driver.get("https://sys.ndhu.edu.tw/gc/sportcenter/SportsFields/Query.aspx")
            time.sleep(2)
            if target_date in driver.page_source:
                send_to_discord(f"ℹ️ **週日自動跳過**：偵測到 `{target_date}` 已經有預約紀錄，本週末任務已完成。")
                driver.quit()
                return

        # 3. 執行填表 (傳入計算好的 12 天後日期)
        fill_form(driver, account.firsttime, account.lasttime, account.totalhours, target_date, account.discord_webhook)
        send_to_discord(f"✅ **預約程序執行完畢**\n目標預約日期：`{target_date}`\n請至系統確認是否成功。",account.discord_webhook)

    except Exception as e:
        error_msg = traceback.format_exc()
        send_to_discord(f"❌ **預約執行失敗**\n日期：`{target_date}`\n原因：`{str(e)}`\n詳細錯誤：\n```{error_msg}```",account.discord_webhook)
    finally:
        driver.quit()

# --- 主掛機迴圈 ---
startup_msg = "🤖 **預約機器人已啟動**\n監控中，將於每週六、日 00:00 自動執行預約。"
send_to_discord(startup_msg,account.discord_webhook)

while True:
    # 1. 取得台灣目前的精準時間
    now = get_taiwan_time()
    current_time = now.strftime("%H:%M")
    
    # 2. 每天 00:00 觸發
    if current_time == "00:00":
        # 計算 12 天後的日期物件 (自動處理跨月/潤年)
        target_date_obj = now + datetime.timedelta(days=12)
        target_date_str = target_date_obj.strftime("%Y/%m/%d")
        
        status_report = (
            f"⏰ **時間到！今日日期：{now.strftime('%Y/%m/%d')}**\n"
            f"🎯 預設預約目標（12天後）：`{target_date_str}`"
        )
        send_to_discord(status_report,account.discord_webhook)

        # 3. 判斷今天是不是週六(5)或週日(6)
        if now.weekday() in [5, 6]:
            trigger_msg = f"🚀 **週末觸發預約流程**\n正在嘗試搶購 `{target_date_str}` 的場地..."
            send_to_discord(trigger_msg,account.discord_webhook)
            run_reservation(target_date_str)

        # 避免在 00:00 這一分鐘內重複跑，睡 61 秒
        time.sleep(61)

    time.sleep(1800)