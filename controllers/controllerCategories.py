import datetime
from db import get_db_connection

def get_all_categories():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM category WHERE status = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_category_by_id(category_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM category WHERE id = %s", (category_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_category(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()

    cursor.execute("""
        INSERT INTO category (name, image_id, user_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data.get("name"),
        data.get("image_id"),
        data.get("user_id"),
        data.get("status", 1),
        now,
        now
    ))

    conn.commit()
    category_id = cursor.lastrowid
    conn.close()

    return { "id": category_id, **data }

def update_category(category_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Preserve created_at
    cursor.execute("SELECT created_at FROM category WHERE id = %s", (category_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return { "error": "Category not found" }

    created_at = row["created_at"]
    updated_at = datetime.datetime.now()

    cursor.execute("""
        UPDATE category
        SET name = %s, image_id = %s, user_id = %s, status = %s, created_at = %s, updated_at = %s
        WHERE id = %s
    """, (
        data.get("name"),
        data.get("image_id"),
        data.get("user_id"),
        data.get("status", 1),
        created_at,
        updated_at,
        category_id
    ))

    conn.commit()
    conn.close()

    return { "id": category_id, **data, "created_at": created_at, "updated_at": updated_at }

def delete_category(category_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE category SET status = 0 WHERE id = %s", (category_id,))
    conn.commit()
    conn.close()
    return { "message": f"Category {category_id} soft-deleted (status = 0)" }
