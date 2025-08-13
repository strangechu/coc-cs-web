from flask import Flask, render_template, request, redirect, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
DATABASE = 'characters.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'  # 設定上傳圖片的資料夾

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 初始化資料庫
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                occupation TEXT,
                app TEXT,
                str INTEGER,
                dex INTEGER,
                san INTEGER,
                image TEXT
            )
        ''')
        conn.commit()
        conn.close()

# 首頁（顯示表單）
@app.route("/")
def index():
    return render_template("index.html")

# 表單送出後儲存資料
@app.route("/create", methods=["POST"])
def create():
    name = request.form["name"]
    occupation = request.form["occupation"]
    app_ = request.form["app"]
    str_ = request.form["str"]
    dex = request.form["dex"]
    san = request.form["san"]
    image_filename = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filename = filename
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO characters (name, occupation, app, str, dex, san, image) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (name, occupation, app_, str_, dex, san, image_filename))
    conn.commit()
    conn.close()

    return redirect("/characters")

# 角色列表
@app.route("/characters")
def list_characters():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, name, occupation, app, str, dex, san, image FROM characters")
    characters = c.fetchall()
    conn.close()
    return render_template("list.html", characters=characters)

# 刪除所有角色資料與圖片
@app.route("/clear", methods=["POST"])
def clear_characters():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM characters")
    conn.commit()
    conn.close()
    # 刪除所有角色圖片
    upload_folder = app.config['UPLOAD_FOLDER']
    if os.path.exists(upload_folder):
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    return redirect("/")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
