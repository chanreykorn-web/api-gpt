import datetime
from db import get_db_connection

def create_gallery(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    now = datetime.datetime.now()

    query = """
        INSERT INTO gallery (image_id, user_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        data.get("image_id"),
        data.get("user_id"),
        data.get("status", 1),
        now,
        now
    )
    cursor.execute(query, values)
    conn.commit()
    gallery_id = cursor.lastrowid
    conn.close()

    return { "id": gallery_id, **data }

def get_all_gallery():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gallery WHERE status = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_gallery_by_id(gallery_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gallery WHERE id = %s", (gallery_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_gallery(gallery_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()

    query = """
        UPDATE gallery SET image_id = %s, user_id = %s, status = %s, updated_at = %s
        WHERE id = %s
    """
    values = (
        data.get("image_id"),
        data.get("user_id"),
        data.get("status", 1),
        now,
        gallery_id
    )
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return { "id": gallery_id, **data }

def delete_gallery(gallery_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE gallery SET status = 0 WHERE id = %s", (gallery_id,))
    conn.commit()
    conn.close()
    return { "message": "Gallery soft-deleted" }
