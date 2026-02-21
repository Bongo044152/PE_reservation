# PE_reservation
## 基本資訊
這個程式是用來自動搶場地的，可以讓使用者自行選擇要在甚麼時候的星期幾自動搶場地
## 功能說明
程式啟動後會持續在背景運行，每天固定時間自動檢查今天星期是否需要執行。
程式執行時會預約希望於星期幾的場地。
## 尚未解決問題
目前還沒有將後面破除驗證碼和送出表單的部分做完，請等待
## 安裝與使用
### 1. 建立虛擬環境
```bash
python -m venv venv
```

### 2. 啟動虛擬環境(參考指令)
#### Windows (cmd)
```shell
venv\Scripts\activate
```

#### Windows (PowerShell)
```shell
venv\Scripts\Activate.ps1
```

#### macOS / Linux
```bash
source venv/Scripts/activate
```

### 3. 安裝依賴套件
```bash
pip install -r requirements.txt`
```

### 4. 填入user_config中的資料
把資料填入 user_config 中

### 5. 執行程式
```bash
python main.py
```

