import datetime
from db import get_db_connection

def get_all_spicifications():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM spicification WHERE status = 1")
    result = cursor.fetchall()
    conn.close()
    return result

def get_spicification_by_id(spicification_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM spicification WHERE id = %s", (spicification_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def create_spicification(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if user_id exists
    cursor.execute("SELECT id FROM users WHERE id = %s", (data.get("user_id"),))
    if not cursor.fetchone():
        conn.close()
        return {"error": "user_id not found"}

    now = datetime.datetime.now()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO spicification (category, category_sub, title, dis, user_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("category"),
        data.get("category_sub"),
        data.get("title"),
        data.get("dis"),
        data.get("user_id"),
        data.get("status", 1),
        now,
        now
    ))

    conn.commit()
    spicification_id = cursor.lastrowid
    conn.close()

    return { "id": spicification_id, **data }

def update_spicification(spicification_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT created_at FROM spicification WHERE id = %s", (spicification_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"error": "Spicification not found"}

    created_at = row["created_at"]
    updated_at = datetime.datetime.now()

    cursor.execute("""
        UPDATE spicification SET category = %s, category_sub = %s, title = %s, dis = %s, user_id = %s, 
        status = %s, created_at = %s, updated_at = %s WHERE id = %s
    """, (
        data.get("category"),
        data.get("category_sub"),
        data.get("title"),
        data.get("dis"),
        data.get("user_id"),
        data.get("status", 1),
        created_at,
        updated_at,
        spicification_id
    ))

    conn.commit()
    conn.close()

    return { "id": spicification_id, **data }

def delete_spicification(spicification_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE spicification SET status = 0 WHERE id = %s", (spicification_id,))
    conn.commit()
    conn.close()
    return { "message": f"Spicification {spicification_id} soft-deleted" }
