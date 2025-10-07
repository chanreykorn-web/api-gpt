import datetime
from db import get_db_connection

def get_all_banners():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.*, g.image_id AS gallery_image
        FROM banner b
        LEFT JOIN gallery g ON b.image_id = g.id
        WHERE b.status = 1
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_banner_by_id(banner_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM banner WHERE id = %s", (banner_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_banner(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Validate user_id
    cursor.execute("SELECT id FROM users WHERE id = %s", (data.get("user_id"),))
    if not cursor.fetchone():
        conn.close()
        return {"error": "user_id not found"}

    now = datetime.datetime.now()
    cursor.execute("""
        INSERT INTO banner (image_id, path, user_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data.get("image_id"),
        data.get("path"),
        data.get("user_id"),
        data.get("status", 1),
        now,
        now
    ))

    conn.commit()
    banner_id = cursor.lastrowid
    conn.close()
    return {"id": banner_id, **data}

def update_banner(banner_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get existing created_at
    cursor.execute("SELECT created_at FROM banner WHERE id = %s", (banner_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return { "error": "Banner not found" }

    created_at = row["created_at"]
    updated_at = datetime.datetime.now()

    cursor.execute("""
        UPDATE banner SET image_id = %s, title = %s, path = %s, user_id = %s, status = %s, created_at = %s, updated_at = %s
        WHERE id = %s
    """, (
        data.get("image_id"),
        data.get("title"),
        data.get("path"),
        data.get("user_id"),
        data.get("status", 1),
        created_at,
        updated_at,
        banner_id
    ))

    conn.commit()
    conn.close()
    return { "id": banner_id, **data, "created_at": created_at, "updated_at": updated_at }

def delete_banner(banner_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE banner SET status = 0 WHERE id = %s", (banner_id,))
    conn.commit()
    conn.close()
    return { "message": f"Banner {banner_id} soft-deleted (status = 0)" }


def get_banner_by_type(banner_type: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.*, g.image_id AS gallery_image
        FROM banner b
        LEFT JOIN gallery g ON b.image_id = g.id
        WHERE b.status = 1 AND b.type = %s
        ORDER BY b.updated_at DESC
        LIMIT 1
    """, (banner_type,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_banner_by_type(banner_type: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.*, g.image_id AS gallery_image
        FROM banner b
        LEFT JOIN gallery g ON b.image_id = g.id
        WHERE b.status = 1 AND b.type = %s
        ORDER BY b.updated_at DESC
        LIMIT 1
    """, (banner_type,))
    row = cursor.fetchone()
    conn.close()
    return row


def set_banner_type(banner_id: int, banner_type: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE banner SET type = %s WHERE id = %s", (banner_type, banner_id))
    conn.commit()
    conn.close()
    return { "message": f"Banner {banner_id} type set to {banner_type}" }