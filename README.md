
# COC 角色卡儲存網站

這是一個使用 Python + Flask 製作的 Call of Cthulhu（COC）TRPG 角色卡儲存系統，支援建立角色、儲存到 SQLite 資料庫、瀏覽所有角色。

## 📁 專案結構

```
coc-cs-web/
├── app.py               ← Flask 主程式
├── requirements.txt     ← Python 套件依賴列表
├── venv/                ← 虛擬環境（不需提交）
├── characters.db        ← SQLite 資料庫（啟動時自動產生）
├── templates/
│   ├── index.html       ← 角色建立表單
│   └── list.html        ← 角色列表頁
```

---

## 🚀 開發環境啟動步驟（Windows）

### 1️⃣ 進入專案資料夾

```bash
cd F:\Projects\coc-cs-web
```

### 2️⃣ 啟動 Python 虛擬環境

- 如果你使用的是 PowerShell：
  ```powershell
  venv\Scripts\Activate.ps1
  ```

- 如果你使用的是 CMD：
  ```cmd
  venv\Scripts\activate.bat
  ```

### 3️⃣ 安裝依賴套件

若尚未安裝或虛擬環境為全新建立，請執行：

```bash
pip install -r requirements.txt
```

---

### 4️⃣ 啟動 Flask 開發伺服器

```bash
python app.py
```

接著開啟瀏覽器前往：
```
http://localhost:5000/
```

---

## 📦 套件依賴列表（自動生成於 requirements.txt）

- Flask

---

## 📌 備註

- 資料會儲存在本地的 `characters.db` 檔案中
- 所有角色資料均透過 HTML 表單送出並儲存於 SQLite
- 上線部署時請參考 `gunicorn + nginx` 的說明（另附）

---

## 🛠 建議指令備忘

重新建立虛擬環境時：

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
