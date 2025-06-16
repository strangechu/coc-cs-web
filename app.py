from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'characters.db'

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
                san INTEGER
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

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO characters (name, occupation, app, str, dex, san) VALUES (?, ?, ?, ?, ?, ?)",
              (name, occupation, app_, str_, dex, san))
    conn.commit()
    conn.close()

    return redirect("/characters")

# 角色列表
@app.route("/characters")
def list_characters():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, name, occupation, app, str, dex, san FROM characters")
    characters = c.fetchall()
    conn.close()
    return render_template("list.html", characters=characters)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
