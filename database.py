import sqlite3

# اتصال به دیتابیس
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# ذخیره‌سازی اطلاعات کاربر
def save_user_info(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (user_id, points) VALUES (?, ?)", (user_id, 1000))
    conn.commit()
    conn.close()

# دریافت امتیاز کاربر
def get_user_points(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT points FROM users WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    conn.close()
    return result['points'] if result else 0

# اضافه کردن امتیاز به کاربر
def add_points(user_id, points):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (points, user_id))
    conn.commit()
    conn.close()

# کسر امتیاز از کاربر
def subtract_points(user_id, points):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET points = points - ? WHERE user_id = ?", (points, user_id))
    conn.commit()
    conn.close()

# ایجاد جدول‌ها در دیتابیس
def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            points INTEGER
        )
    """)
    conn.commit()
    conn.close()

create_tables()
