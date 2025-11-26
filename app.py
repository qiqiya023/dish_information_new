from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

DB = "menu.db"

app = Flask(__name__)
CORS(app)


def query_db(query, args=(), one=False):
    """查询数据库"""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    conn.close()
    if one:
        return dict(rows[0]) if rows else None
    return [dict(r) for r in rows]


@app.route("/")
def home():
    return "Canteen Menu API is running!"


# ① 查询菜品（支持条件过滤）
@app.route("/dishes", methods=["GET"])
def search_dishes():
    floor = request.args.get("floor")
    stall = request.args.get("stall")
    taste = request.args.get("taste")
    category = request.args.get("category")
    max_price = request.args.get("max_price")

    query = "SELECT * FROM dishes WHERE 1=1"
    params = []

    if floor:
        query += " AND floor = ?"
        params.append(floor)

    if stall:
        query += " AND stall_name = ?"
        params.append(stall)

    if taste:
        query += " AND taste_tag = ?"
        params.append(taste)

    if category:
        query += " AND category = ?"
        params.append(category)

    if max_price:
        query += " AND price <= ?"
        params.append(float(max_price))

    results = query_db(query, params)
    return jsonify({"count": len(results), "results": results})


# ② 随机推荐一个今日供应的菜
@app.route("/random", methods=["GET"])
def random_dish():
    row = query_db(
        "SELECT * FROM dishes WHERE is_available_today='是' ORDER BY RANDOM() LIMIT 1",
        one=True
    )
    return jsonify(row if row else {})


@app.route("/stalls", methods=["GET"])
def list_stalls():
    rows = query_db("SELECT DISTINCT stall_name FROM dishes")
    stalls = [row["stall_name"] for row in rows]
    # 包装成 JSON 对象，不要直接返回数组！
    return jsonify({"stalls": stalls})

# ④ 获取所有楼层
@app.route("/floors", methods=["GET"])
def list_floors():
    rows = query_db("SELECT DISTINCT floor FROM dishes")
    floors = [row["floor"] for row in rows]
    return jsonify({"floors": floors})  # ✅ 包装成对象


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
