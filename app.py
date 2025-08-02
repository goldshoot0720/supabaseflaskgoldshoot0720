from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client
import os

# 載入環境變數
load_dotenv()

# 初始化 Flask 應用
app = Flask(__name__)
CORS(app)

# 連接 Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 允許查詢的資料表
ALLOWED_TABLES = {
    "article", "bank", "cloud", "experience", "food", "host",
    "inventory", "mail", "member", "routine", "subscription", "video"
}

# 查詢資料表
def select_table(table_name):
    if table_name not in ALLOWED_TABLES:
        raise Exception(f"❌ Table '{table_name}' is not allowed.")

    # 執行查詢
    result = supabase.table(table_name).select("*").execute()
    return result.data

# 首頁列出所有表格
@app.route("/")
def index():
    links = ''.join(f'<li><a href="/{name}">{name}</a></li>' for name in sorted(ALLOWED_TABLES))
    return f"<h1>Supabase Tables</h1><ul>{links}</ul>"

# 動態路由查詢資料
@app.route("/<table_name>")
def get_table(table_name):
    try:
        data = select_table(table_name)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 啟動伺服器
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
