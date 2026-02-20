# Configuration file for PE reservation script

# website URL
# NOTE: 請勿更改此 URL，除非網站有變更
WEBSITE_URL = "https://sys.ndhu.edu.tw/gc/sportcenter/SportsFields/Login.aspx"

# program settings
execution_days = [5, 6]  # Monday == 0 ... Sunday == 6.
execution_time = "00:00"  # 預約每天程式執行時間 (24小時制，格式: "HH:MM")

# User credentials: account and password
account = ""
password = ""

# Reservation settings
firsttime = 12  # 搜尋開始時段 (24小時制)
lasttime = 17  # 搜尋結束時段 (24小時制)
totalhours = 2  # 期望預約總時數
discord_webhooks: list[str] = []  # Discord Webhook URL list
sleeping_time = 1
