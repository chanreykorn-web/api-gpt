import datetime
from db import get_db_connection

def get_all_choose_us():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM choose_us WHERE status = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_choose_us_by_id(choose_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM choose_us WHERE id = %s", (choose_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_choose_us(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()

    # Validate user_id
    cursor.execute("SELECT id FROM users WHERE id = %s", (data.get("user_id"),))
    if not cursor.fetchone():
        conn.close()
        return {"error": "user_id not found"}

    cursor.execute("""
        INSERT INTO choose_us (icon, title, category, category_sub, user_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("icon"),
        data.get("title"),
        data.get("category"),
        data.get("category_sub"),
        data.get("user_id"),
        data.get("status", 1),
        now,
        now
    ))

    conn.commit()
    choose_id = cursor.lastrowid
    conn.close()
    return {"id": choose_id, **data, "created_at": now, "updated_at": now}

def update_choose_us(choose_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT created_at FROM choose_us WHERE id = %s", (choose_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"error": "Choose Us item not found"}

    created_at = row["created_at"]
    updated_at = datetime.datetime.now()

    cursor.execute("""
        UPDATE choose_us SET icon=%s, title=%s, category=%s, category_sub=%s, user_id=%s, status=%s,
        created_at=%s, updated_at=%s WHERE id=%s
    """, (
        data.get("icon"),
        data.get("title"),
        data.get("category"),
        data.get("category_sub"),
        data.get("user_id"),
        data.get("status", 1),
        created_at,
        updated_at,
        choose_id
    ))

    conn.commit()
    conn.close()
    return {"id": choose_id, **data, "created_at": created_at, "updated_at": updated_at}

def delete_choose_us(choose_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE choose_us SET status = 0 WHERE id = %s", (choose_id,))
    conn.commit()
    conn.close()
    return {"message": f"Choose Us {choose_id} soft-deleted"}
