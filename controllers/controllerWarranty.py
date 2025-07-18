import datetime
from db import get_db_connection

def get_all_warranties():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM warranty WHERE status = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_warranty_by_id(warranty_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM warranty WHERE id = %s", (warranty_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_warranty(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Validate foreign keys
    cursor.execute("SELECT id FROM gallery WHERE id = %s", (data.get("image_id"),))
    if not cursor.fetchone():
        conn.close()
        return {"error": "image_id not found"}

    cursor.execute("SELECT id FROM users WHERE id = %s", (data.get("user_id"),))
    if not cursor.fetchone():
        conn.close()
        return {"error": "user_id not found"}

    now = datetime.datetime.now()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO warranty (title, dis, title_contact, name, phone, email, image_id, user_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("title"),
        data.get("dis"),
        data.get("title_contact"),
        data.get("name"),
        data.get("phone"),
        data.get("email"),
        data.get("image_id"),
        data.get("user_id"),
        data.get("status", 1),
        now,
        now
    ))

    conn.commit()
    warranty_id = cursor.lastrowid
    conn.close()
    return { "id": warranty_id, **data }

def update_warranty(warranty_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT created_at FROM warranty WHERE id = %s", (warranty_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return { "error": "Warranty not found" }

    created_at = row["created_at"]
    updated_at = datetime.datetime.now()

    cursor.execute("""
        UPDATE warranty SET
        title = %s,
        dis = %s,
        title_contact = %s,
        name = %s,
        phone = %s,
        email = %s,
        image_id = %s,
        user_id = %s,
        status = %s,
        created_at = %s,
        updated_at = %s
        WHERE id = %s
    """, (
        data.get("title"),
        data.get("dis"),
        data.get("title_contact"),
        data.get("name"),
        data.get("phone"),
        data.get("email"),
        data.get("image_id"),
        data.get("user_id"),
        data.get("status", 1),
        created_at,
        updated_at,
        warranty_id
    ))

    conn.commit()
    conn.close()
    return { "id": warranty_id, **data }

def delete_warranty(warranty_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE warranty SET status = 0 WHERE id = %s", (warranty_id,))
    conn.commit()
    conn.close()
    return { "message": f"Warranty {warranty_id} soft-deleted" }
