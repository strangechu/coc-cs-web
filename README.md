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

---

## 部署到 Linux 伺服器（以 Linode Debian 為例）

1. **安裝必要套件**
   ```sh
   sudo apt update
   sudo apt install python3 python3-pip python3-venv nginx git
   ```

2. **取得原始碼**
   ```sh
   git clone <你的 GitHub 專案網址>
   cd coc-cs-web
   ```

3. **建立虛擬環境並安裝依賴**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **測試 Flask 應用**
   ```sh
   python app.py
   ```
   確認能正常啟動（預設 http://localhost:5000）。

5. **使用 Gunicorn 部署 Flask**
   ```sh
   pip install gunicorn
   gunicorn -w 4 app:app
   ```
   Gunicorn 預設監聽 8000 port，可依需求調整。

6. **Nginx 設定（共存 PHP 與 Flask）**
   - PHP 網頁維持原本設定（如 `/`）。
   - Flask 服務掛載於 `/coc-web` 路徑：

     ```
     location /coc-web/ {
         proxy_pass http://127.0.0.1:8000/;
         proxy_set_header Host $host;
         proxy_set_header X-Real-IP $remote_addr;
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
         proxy_set_header X-Forwarded-Proto $scheme;
         # proxy_set_header SCRIPT_NAME /coc-web; # 可註解，除非 Flask 需支援 SCRIPT_NAME
     }
     location /coc-web/static/ {
         alias /root/coc-cs-web/static/;
     }
     ```

   - 若遇 `Bad Request: Request path '/' does not start with SCRIPT_NAME '/coc-web'`，可將 `proxy_set_header SCRIPT_NAME /coc-web;` 註解掉，或於 Flask 端使用 DispatcherMiddleware 處理前綴。

7. **檢查 Nginx 設定語法並重啟**
   ```sh
   sudo nginx -t
   sudo systemctl restart nginx
   ```

8. **檢查 static/uploads 權限**
   ```sh
   mkdir -p static/uploads
   chmod 755 static/uploads
   ```

9. **.gitignore 設定**
   - `.db` 檔案與 `static/uploads/` 目錄不建議加入版本控管，請參考 `.gitignore` 範例。

10. **存取服務**
    - PHP 網頁：`http://your_domain/`
    - Flask 服務：`http://your_domain/coc-web/`

---

如遇特殊路徑或 SCRIPT_NAME 問題，請依實際需求調整 Nginx 及 Flask 設定。
