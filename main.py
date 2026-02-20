import datetime, time  # 用來處理時間相關
import pytz

# debug 用，用來取得完整錯誤堆疊字串
# see: https://docs.python.org/zh-tw/3.8/library/traceback.html
import traceback

# Selenium
from utils.webdriver import get_driver

# configs
import user_config
from user_config import WEBSITE_URL
from utils.dev_config import DEBUG_MODE

# modules
from modules.login import login
from modules.form import fill_form
from modules.discord import send_to_discord

# logger setup
import logging

logger = logging.getLogger(__name__)


def get_taiwan_time():
    tw_tz = pytz.timezone("Asia/Taipei")
    return datetime.datetime.now(tw_tz)


def run_reservation(target_date):
    driver = get_driver()
    try:
        # 1. 前往登入
        driver.get(WEBSITE_URL)
        time.sleep(user_config.sleeping_time)
        login(
            driver, user_config.account, user_config.password, user_config.sleeping_time
        )
        time.sleep(user_config.sleeping_time)
        logger.debug("Login successful.")

        # 2. 執行填表 (傳入計算好的 12 天後日期)
        fill_form(
            driver,
            user_config.firsttime,
            user_config.lasttime,
            user_config.totalhours,
            target_date,
            user_config.sleeping_time,
        )
        send_to_discord(
            f"✅ **預約程序執行完畢**\n目標預約日期：`{target_date}`\n請至系統確認是否成功。",
        )

    except Exception as e:
        error_msg = traceback.format_exc()
        send_to_discord(
            f"❌ **預約執行失敗**\n原因：`{str(e)}`",
        )
        logger.error(f"Exception during reservation process:\n{error_msg}")
    finally:
        driver.quit()


def main():
    # --- 主掛機迴圈 ---
    startup_msg = f"🤖 **預約機器人已啟動**\n監控中，將於每週六、日 {user_config.execution_time} 自動執行預約。"
    send_to_discord(startup_msg)

    while True:
        # 1. 取得台灣目前的精準時間
        now = get_taiwan_time()
        current_time = now.strftime("%H:%M")

        # 2. 按照使用者設定的時間觸發
        if (
            current_time == user_config.execution_time
            and (now.weekday()+5)%7 in user_config.execution_days
        ) or DEBUG_MODE:
            logger.info("Time reached, starting reservation process.")

            # 計算 12 天後的日期物件 (自動處理跨月/潤年)
            target_date_obj = now + datetime.timedelta(days=12)
            target_date_str = target_date_obj.strftime("%Y/%m/%d")

            status_report = (
                f"⏰ **時間到！今日日期：{now.strftime('%Y/%m/%d')}**\n"
                f"🎯 預設預約目標（12天後）：`{target_date_str}`"
            )
            send_to_discord(status_report)
            run_reservation(target_date_str)
        now = get_taiwan_time()
        user_hour, user_minute = map(int, user_config.execution_time.split(":"))
        tomorrow = (now + datetime.timedelta(days=1)).replace(hour=user_hour, minute=user_minute, second=0, microsecond=0)
        seconds_to_midnight = (tomorrow - now).total_seconds()
        time.sleep(seconds_to_midnight)


if __name__ == "__main__":
    main()
