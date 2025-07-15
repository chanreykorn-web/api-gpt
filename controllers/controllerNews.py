import datetime
from db import get_db_connection

def get_all_news():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM news WHERE status = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_news_by_id(news_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM news WHERE id = %s", (news_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_news(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Validate foreign keys
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
        INSERT INTO news (title, image_id, detail, banner_id, user_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("title"),
        data.get("image_id"),
        data.get("detail"),
        data.get("banner_id"),
        data.get("user_id"),
        data.get("status", 1),
        now,
        now
    ))
    conn.commit()
    news_id = cursor.lastrowid
    conn.close()
    return {"id": news_id, **data}

def update_news(news_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT created_at FROM news WHERE id = %s", (news_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"error": "News not found"}

    created_at = row["created_at"]
    updated_at = datetime.datetime.now()

    cursor.execute("""
        UPDATE news SET title=%s, image_id=%s, detail=%s, banner_id=%s,
        user_id=%s, status=%s, created_at=%s, updated_at=%s WHERE id = %s
    """, (
        data.get("title"),
        data.get("image_id"),
        data.get("detail"),
        data.get("banner_id"),
        data.get("user_id"),
        data.get("status", 1),
        created_at,
        updated_at,
        news_id
    ))
    conn.commit()
    conn.close()
    return {"id": news_id, **data, "created_at": created_at, "updated_at": updated_at}

def delete_news(news_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE news SET status = 0 WHERE id = %s", (news_id,))
    conn.commit()
    conn.close()
    return {"message": f"News {news_id} soft-deleted (status = 0)"}