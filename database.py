import sqlite3

# 🔹 Bog'lanish funksiyasi
def get_connect():
    return sqlite3.connect("database.db")


# 🔹 Jadval yaratish
def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with get_connect() as db:
        cur = db.cursor()
        cur.execute(sql)
        db.commit()


# 🔹 Vazifani qo‘shish
def add_task(user_id, name):
    sql = "INSERT INTO tasks (user_id, name) VALUES (?, ?)"
    with get_connect() as db:
        cur = db.cursor()
        cur.execute(sql, (user_id, name.strip()))
        db.commit()


# 🔹 Statusga qarab olish (All, Pending, Done)
def get_tasks_by_status(user_id, status):
    with get_connect() as db:
        cur = db.cursor()
        if status == "all":
            cur.execute("SELECT name, status FROM tasks WHERE user_id = ?", (user_id,))
        elif status == "pending":
            cur.execute("SELECT name, status FROM tasks WHERE user_id = ? AND status = 'pending'", (user_id,))
        elif status == "done":
            cur.execute("SELECT name, status FROM tasks WHERE user_id = ? AND status = 'done'", (user_id,))
        else:
            return []

        rows = cur.fetchall()
        return [{"name": row[0], "status": row[1]} for row in rows]


# 🔹 Vazifa nomini o‘zgartirish
def update_task_name(user_id, old_name, new_name):
    with get_connect() as db:
        cur = db.cursor()
        cur.execute(
            "UPDATE tasks SET name = ? WHERE user_id = ? AND name = ?",
            (new_name.strip(), user_id, old_name.strip())
        )
        db.commit()
        return cur.rowcount > 0


# 🔹 Vazifa holatini (status) o‘zgartirish
def update_task_status(user_id, task_name, new_status):
    with get_connect() as db:
        cur = db.cursor()
        cur.execute(
            "UPDATE tasks SET status = ? WHERE user_id = ? AND name = ?",
            (new_status.lower(), user_id, task_name.strip())
        )
        db.commit()
        return cur.rowcount > 0


# 🔹 Vazifani o‘chirish
def delete_task(user_id, task_name):
    task_name = task_name.strip().lower()
    with get_connect() as db:
        cur = db.cursor()
        sql = "DELETE FROM tasks WHERE user_id = ? AND LOWER(name) = ?"
        cur.execute(sql, (user_id, task_name))
        db.commit()
        return cur.rowcount > 0
