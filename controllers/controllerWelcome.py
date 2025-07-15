import datetime
from db import get_db_connection

# Get all welcome entries
def get_all_welcome():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM welcome WHERE status = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Get welcome by ID
def get_welcome_by_id(welcome_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM welcome WHERE id = %s", (welcome_id,))
    row = cursor.fetchone()
    conn.close()
    return row

# Create welcome entry
def create_welcome(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check foreign keys
    cursor.execute("SELECT id FROM gallery WHERE id = %s", (data.get("image_id"),))
    if not cursor.fetchone():
        conn.close()
        return {"error": "image_id not found"}

    cursor.execute("SELECT id FROM banner WHERE id = %s", (data.get("banner_id"),))
    if not cursor.fetchone():
        conn.close()
        return {"error": "banner_id not found"}

    cursor.execute("SELECT id FROM users WHERE id = %s", (data.get("user_id"),))
    if not cursor.fetchone():
        conn.close()
        return {"error": "user_id not found"}

    now = datetime.datetime.now()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO welcome (title, detail, image_id, banner_id, user_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("title"),
        data.get("detail"),
        data.get("image_id"),
        data.get("banner_id"),
        data.get("user_id"),
        data.get("status", 1),
        now,
        now
    ))
    conn.commit()
    welcome_id = cursor.lastrowid
    conn.close()
    return {"id": welcome_id, **data}

# Update welcome entry
def update_welcome(welcome_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Preserve created_at
    cursor.execute("SELECT created_at FROM welcome WHERE id = %s", (welcome_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"error": "Welcome not found"}

    created_at = row["created_at"]
    updated_at = datetime.datetime.now()

    cursor.execute("""
        UPDATE welcome
        SET title = %s, detail = %s, image_id = %s, banner_id = %s, user_id = %s,
            status = %s, created_at = %s, updated_at = %s
        WHERE id = %s
    """, (
        data.get("title"),
        data.get("detail"),
        data.get("image_id"),
        data.get("banner_id"),
        data.get("user_id"),
        data.get("status", 1),
        created_at,
        updated_at,
        welcome_id
    ))
    conn.commit()
    conn.close()
    return {"id": welcome_id, **data, "created_at": created_at, "updated_at": updated_at}

# Soft delete welcome entry
def delete_welcome(welcome_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE welcome SET status = 0 WHERE id = %s", (welcome_id,))
    conn.commit()
    conn.close()
    return {"message": f"Welcome {welcome_id} soft-deleted (status = 0)"}
