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
        INSERT INTO choose_us (image_id, title, category, category_sub, descriptions, path, user_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("image_id"),
        data.get("title"),
        data.get("category"),
        data.get("category_sub"),
        data.get("descriptions"),
        data.get("path"),
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
        UPDATE choose_us SET image_id=%s, title=%s, category=%s, category_sub=%s, descriptions=%s, path=%s, user_id=%s, status=%s,
        created_at=%s, updated_at=%s WHERE id=%s
    """, (
        data.get("image_id"),
        data.get("title"),
        data.get("category"),
        data.get("category_sub"),
        data.get("descriptions"),
        data.get("path"),
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


def get_all_choose_us_public():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM choose_us WHERE status = 1 ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_process_public(choose_id: int, data: dict):
    """
    Update only the 'our_process' field for a product.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # ✅ Check if product exists
        cursor.execute("SELECT id FROM choose_us WHERE id = %s", (choose_id,))
        row = cursor.fetchone()
        if not row:
            return {"success": False, "error": "choose us not found"}

        # ✅ Update only 'new' field
        cursor.execute("""
            UPDATE choose_us 
            SET our_process = %s,
                updated_at = %s
            WHERE id = %s
        """, (
            data.get("our_process"),
            datetime.datetime.utcnow(),  # use UTC for consistency
            choose_id
        ))

        conn.commit()
        return {"success": True, "id": choose_id, "our_process": data.get("our_process")}

    except Exception as e:
        conn.rollback()
        return {"success": False, "error": str(e)}

    finally:
        cursor.close()
        conn.close()
        
        
def get_choose_us_by_id_public(choose_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM choose_us WHERE id = %s", (choose_id,))
    row = cursor.fetchone()
    conn.close()
    return row