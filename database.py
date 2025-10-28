from psycopg2 import connect
from environs import Env

env = Env()
env.read_env()

# 🔹 Bog'lanish funksiyasi
def get_connect():
    conn=connect(
        user=env.str("USER"),
        password=env.str("PASSWORD"),
        host=env.str("HOST"),
        port=env.str("PORT"),
        database=env.str("DATABASE")
    )
    conn.set_client_encoding('UTF8')
    return conn

# 🔹 Jadval yaratish
def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS tasks(
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        name VARCHAR(1000) NOT NULL,
        status VARCHAR(100) NOT NULL DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with get_connect() as db:
        with db.cursor() as cur:
            cur.execute(sql)
            db.commit()

# 🔹 Vazifani qo‘shish
def add_task(user_id, name):
    sql = "INSERT INTO tasks (user_id, name) VALUES (%s, %s)"
    with get_connect() as db:
        with db.cursor() as cur:
            cur.execute(sql, (user_id, name))
            db.commit()

# 🔹 Statusga qarab olish (All, Pending, Done)
def get_tasks_by_status(user_id, status):
    with get_connect() as conn:
        with conn.cursor() as cur:
            if status == "all":
                cur.execute("SELECT name, status FROM tasks WHERE user_id = %s", (user_id,))
            elif status == "pending":
                cur.execute("SELECT name, status FROM tasks WHERE user_id = %s AND status = 'pending'", (user_id,))
            elif status == "done":
                cur.execute("SELECT name, status FROM tasks WHERE user_id = %s AND status = 'done'", (user_id,))
            else:
                return []

            rows = cur.fetchall()
            return [{"name": row[0], "status": row[1]} for row in rows]
        
        
# 🔹 Vazifa nomini o‘zgartirish
def update_task_name(user_id, old_name, new_name):
    conn = get_connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET name = %s WHERE user_id = %s AND name = %s",
        (new_name, user_id, old_name)
    )

    conn.commit()
    conn.close()
    return cursor.rowcount > 0  # Agar 1 ta bo‘lsa True qaytaradi


# 🔹 Vazifa holatini (status) o‘zgartirish
def update_task_status(user_id, task_name, new_status):
    conn = get_connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status = %s WHERE user_id = %s AND name = %s",
        (new_status, user_id, task_name)
    )

    conn.commit()
    conn.close()
    return cursor.rowcount > 0


# 🔹 Vazifani o‘chirish 
def delete_task(user_id, task_name):
    task_name = task_name.strip()  

    conn = get_connect()
    cursor = conn.cursor()

  
    sql = "DELETE FROM tasks WHERE user_id = %s::bigint AND LOWER(name) = LOWER(%s)"
    cursor.execute(sql, (user_id, task_name))

    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()

    print(f"[DEBUG] Deleted count: {deleted_count}")  
    return deleted_count > 0

