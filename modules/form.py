import time

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver

from modules.discord import send_to_discord
from modules.captcha import solve_captcha

# logger setup
import logging

logger = logging.getLogger(__name__)


def fill_form(
    driver: webdriver.Chrome,
    firsttime: int,
    lasttime: int,
    totalhours: int,
    target_date: str,
    sleeping_time: int,
):
    first_select = Select(driver.find_element(By.ID, "MainContent_drpkind"))
    first_select.select_by_visible_text("體育館")
    time.sleep(sleeping_time)

    all_results = []

    venues = [
        "XGMB1壽館場B-羽1",
        "XGMB2壽館場B-羽2",
        "XGMB3壽館場B-羽3",
        "XGMB4壽館場B-羽4",
        "XGMC1壽館場C-排1",
        "XGMC2壽館場C-排2",
        "XGMC3壽館場C-排3",
        "XGMC4壽館場C-排4",
    ]

    for venue in venues:
        res = collect_time(driver, venue, target_date)
        all_results.append(res)
        time.sleep(sleeping_time)

    venue_dict = {venues[i]: all_results[i] for i in range(len(venues))}
    final_plan = find_best_combination(venue_dict, firsttime, lasttime, totalhours)
    if final_plan:
        for i in final_plan:
            auto_click_plan(driver, final_plan, target_date, sleeping_time)
    """ to do """
    """剩下通過驗證碼和送出表單的部分"""
    time.sleep(sleeping_time)


def collect_time(
    driver: webdriver.Chrome, place_name: str, target_date: str, sleeping_time: int
) -> list[str]:
    select = Select(driver.find_element(By.ID, "MainContent_DropDownList1"))
    select.select_by_visible_text(place_name)
    time.sleep(sleeping_time)

    click_button = driver.find_element(By.ID, "MainContent_Button1")
    click_button.click()
    time.sleep(sleeping_time)

    results = get_available_slots(driver, target_date)
    return results


def get_available_slots(
    driver: webdriver.Chrome, target_date: str
) -> list[str]:
    # 1. 先抓到日期標題的元素，用它當作「準心」
    date_header = driver.find_element(
        By.XPATH, f"//*[contains(text(), '{target_date}')]"
    )

    # 取得日期標題的左邊界位置
    target_x = date_header.location["x"]
    # 取得日期標題的寬度，算出中心點位置更準
    target_center = target_x + (date_header.size["width"] / 2)

    # 2. 抓取頁面上「所有」含有申請字樣的元素
    # 注意：這裡改用 By.XPATH 抓取所有可能包含「申請」的 a 標籤或 div
    all_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '申請')]")

    available_slots = []

    # 3. 過濾：只有 X 軸位置跟日期標題對齊的，才是我們要的
    for elem in all_elements:
        elem_x = elem.location["x"]
        elem_center = elem_x + (elem.size["width"] / 2)

        # 允許 10 像素以內的誤差（對齊判斷）
        if abs(elem_center - target_center) < 10:
            # 嘗試抓取這個儲存格內的時間文字
            # 通常時間會在同一列的第一欄，或者該元素本身的文字裡
            slot_info = elem.text.strip()
            available_slots.append(slot_info)

    return available_slots


def find_best_combination(all_venues, my_start, my_end, target_duration):
    flat_slots = []
    for venue, slots in all_venues.items():
        for s in slots:
            time_range = s.split("]")[-1]
            s_time, e_time = map(int, time_range.split("~"))
            if s_time >= my_start and e_time <= my_end:
                flat_slots.append((s_time, e_time, venue))

    flat_slots.sort()

    for i in range(len(flat_slots)):
        current_combination = [flat_slots[i]]
        current_total = flat_slots[i][1] - flat_slots[i][0]

        if current_total >= target_duration:
            return current_combination

        last_e = flat_slots[i][1]
        for j in range(i + 1, len(flat_slots)):
            next_s, next_e, next_venue = flat_slots[j]

            if next_s == last_e:
                current_combination.append(flat_slots[j])
                current_total += next_e - next_s
                last_e = next_e

                if current_total >= target_duration:
                    return current_combination

    return None


def auto_click_plan(driver, plan, target_date, sleeping_time):
    try:
        for start, end, venue_name in plan:
            # 1. 切換場地並查詢
            select = Select(driver.find_element(By.ID, "MainContent_DropDownList1"))
            select.select_by_visible_text(venue_name)
            time.sleep(sleeping_time)
            driver.find_element(By.ID, "MainContent_Button1").click()
            time.sleep(sleeping_time)

            # 2. 定位日期 X 座標 (確保點對天)
            date_header = driver.find_element(
                By.XPATH, f"//*[contains(text(), '{target_date}')]"
            )
            target_center = date_header.location["x"] + (date_header.size["width"] / 2)

            # 3. 尋找目標按鈕
            target_time = f"{start:02d}~{end:02d}"
            # 找所有包含時段的按鈕
            candidate_btns = driver.find_elements(
                By.XPATH,
                f"//button[contains(., '{target_time}') and contains(., '申請')]",
            )

            found = False
            for btn in candidate_btns:
                btn_center = btn.location["x"] + (btn.size["width"] / 2)
                if abs(btn_center - target_center) < 10:
                    btn.click()
                    success_msg = f"✅ 申請成功點擊 {venue_name} 的 {target_time}"
                    send_to_discord(success_msg)
                    found = True
                    break

            if not found:
                raise Exception(
                    f"找不到 {target_date} 的 {target_time} 申請按鈕，可能已被搶走！"
                )

            # 注意：點擊後若換頁，此迴圈會因找不到下一場地的選單而報錯
            # 建議如果是多個場地，點完第一個後要處理完表單再回來
    except Exception as e:
        # 這裡會捕捉錯誤並發送，然後再次 raise 讓 main.py 也能接收到
        err_msg = f"❌ **自動點擊階段失敗**\n時段：{target_date}\n原因：{str(e)}"
        send_to_discord(err_msg)
        raise e
