import sqlite3

DB = r"D:\Python\Deepsmoke\app\db.sqlite3"
names = [
    "Популярні товари",
    "Коректори смаку",
    "Аксесуари",
    "Акумулятор",
    "Гіфт бокс",
]
conn = sqlite3.connect(DB)
cur = conn.cursor()
for name in names:
    exists = cur.execute("SELECT 1 FROM app_web_category WHERE name = ? LIMIT 1", (name,)).fetchone()
    if not exists:
        cur.execute(
            "INSERT INTO app_web_category (parent_id, name, image, is_featured) VALUES (?, ?, ?, ?)",
            (None, name, '', 0),
        )
conn.commit()
print(cur.execute("SELECT name FROM app_web_category ORDER BY name").fetchall())
conn.close()
