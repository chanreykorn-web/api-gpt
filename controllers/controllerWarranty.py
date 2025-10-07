from datetime import datetime
from db import get_db_connection 
import datetime

def get_all_warranties():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM warranty")
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

def update_warranty(warranty_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT created_at FROM warranty WHERE id = %s", (warranty_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"error": "Warranty not found"}

    created_at = row["created_at"]
    updated_at = datetime.now()

    cursor.execute("""
        UPDATE warranty SET
            title = %s,
            descriptions = %s,
            image_id = %s,
            user_id = %s,
            status = %s,
            created_at = %s,
            updated_at = %s
        WHERE id = %s
    """, (
        data.get("title"),
        data.get("descriptions"),
        data.get("image_id"),
        data.get("user_id"),
        data.get("status", 1),
        created_at,
        updated_at,
        warranty_id
    ))

    conn.commit()
    conn.close()
    return {"id": warranty_id, **data}

def update_warranty(warranty_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ Check if warranty exists
    cursor.execute("SELECT id FROM warranty WHERE id = %s", (warranty_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"error": "Warranty not found"}

    updated_at = datetime.datetime.now()

    # ✅ Update fields (without touching created_at)
    cursor.execute("""
        UPDATE warranty SET
            title = %s,
            descriptions = %s,
            image_id = %s,
            path = %s,
            user_id = %s,
            status = %s,
            updated_at = %s
        WHERE id = %s
    """, (
        data.get("title"),
        data.get("descriptions"),
        data.get("image_id"),
        data.get("path"),
        data.get("user_id"),
        data.get("status", 1),
        updated_at,
        warranty_id
    ))

    conn.commit()
    conn.close()
    return {"id": warranty_id, "updated_at": updated_at, **data}

def delete_warranty(warranty_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE warranty SET status = 0 WHERE id = %s", (warranty_id,))
    conn.commit()
    conn.close()
    return { "message": f"Warranty {warranty_id} soft-deleted" }


def get_all_warranties_public():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM warranty WHERE status = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows
