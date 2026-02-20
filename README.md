# PE_reservation
## 基本資訊
這個程式是用來自動搶場地的，可以讓使用者自行選擇要在甚麼時候的星期幾自動搶場地
## 安裝與使用
### 1. 建立虛擬環境
` python -m venv venv `
### 2. 啟動虛擬環境
#### windows
`venv\Scripts\activate`
#### macOS / Linux
`source venv/bin/activate`
### 3. 安裝依賴套件
`pip install selenium requests Pillow pytz webdriver-manager`
### 4. 填入user_config中的資料
把資料填入user_config中
### 5. 執行程式
`python main.py`
## 功能說明
程式啟動後會持續在背景運行，每天 00:00 自動檢查今天是否為設定的執行日。
程式執行時會預約希望於星期幾的場地。

## 檔案結構說明

### main.py
程式進入點，負責主迴圈邏輯。每天 00:00 檢查今天是否為設定的執行日，若是則啟動預約流程。

### user_config.py
使用者設定檔，所有個人設定都在這裡填入，包含帳號密碼、執行時段、目標星期幾等。

### modules
#### __init__.py
把 `modules` 資料夾註冊為 Python package，讓其他模組可以透過 `from modules import ...` 的方式引入。包含以下模組：`login`、`form`、`discord`、`captcha`。

#### captcha.py
把圖片中的驗證碼破除，並回傳驗證碼

#### discord.py
負責發送通知到 Discord，包含執行成功、失敗等狀態訊息。

#### form.py
負責爬取每一個場地資訊，根據使用者設定的時段逐一判斷並搶場地，最後送出表單。

#### login.py
負責自動登入網頁，並前往表單頁面。


### utils
#### __init__.py
把 `utils` 資料夾註冊為 Python package，讓其他模組可以透過 `from utils import ...` 的方式引入。

#### dev_config.py
開發環境的設定檔，控制兩件事：
- `DEBUG_MODE`：是否開啟 debug 模式，會影響 log 的詳細程度和 WebDriver 是否顯示視窗
- `WEBDRIVER_CONFIG`：WebDriver 的相關設定，包含是否顯示視窗和自訂 User-Agent

#### webdriver.py
負責建立並回傳一個設定好的 Chrome WebDriver 實例。會根據 `dev_config` 的設定決定是否開啟 headless 模式，並設定 User-Agent 讓爬蟲看起來像一般瀏覽器。