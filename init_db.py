import csv
import sqlite3
import chardet

DB = "menu.db"
CSV_FILE = "dish_information.csv"

# 自动检测文件编码
with open(CSV_FILE, "rb") as f:
    encoding = chardet.detect(f.read())["encoding"]
print("Detected CSV encoding:", encoding)

conn = sqlite3.connect(DB)
c = conn.cursor()

# 建表
c.execute("""
CREATE TABLE IF NOT EXISTS dishes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dish_name TEXT,
    floor TEXT,
    stall_name TEXT,
    category TEXT,
    pricing_type TEXT,
    price REAL,
    unit TEXT,
    taste_tag TEXT,
    is_available_today TEXT
)
""")

# 清空旧数据
c.execute("DELETE FROM dishes")

# 导入 CSV
with open(CSV_FILE, "r", encoding=encoding) as f:
    reader = csv.DictReader(f)
    for row in reader:
        c.execute("""
            INSERT INTO dishes (
                dish_name, floor, stall_name, category,
                pricing_type, price, unit, taste_tag, is_available_today
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["dish_name"],
            row["floor"],
            row["stall_name"],
            row["category"],
            row["pricing_type"],
            float(row["price"]),
            row["unit"],
            row["taste_tag"],
            row["is_available_today"]
        ))

conn.commit()
conn.close()

print("Database initialized successfully!")
