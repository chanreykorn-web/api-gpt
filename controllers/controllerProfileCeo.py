import datetime
from db import get_db_connection

def get_all_ceos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM profile_ceo WHERE status = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_ceo_by_id(ceo_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM profile_ceo WHERE id = %s", (ceo_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_ceo(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check foreign keys
    for field, table in [("image_id", "gallery"), ("user_id", "users")]:
        cursor.execute(f"SELECT id FROM {table} WHERE id = %s", (data.get(field),))
        if not cursor.fetchone():
            conn.close()
            return {"error": f"{field} not found"}

    now = datetime.datetime.now()
    cursor.execute("""
        INSERT INTO profile_ceo (image_id, name, detail, user_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("image_id"),
        data.get("name"),
        data.get("detail"),
        data.get("user_id"),
        data.get("status", 1),
        now,
        now
    ))

    conn.commit()
    ceo_id = cursor.lastrowid
    conn.close()
    return {"id": ceo_id, **data}

def update_ceo(ceo_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT created_at FROM profile_ceo WHERE id = %s", (ceo_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"error": "CEO profile not found"}

    created_at = row["created_at"]
    updated_at = datetime.datetime.now()

    cursor.execute("""
        UPDATE profile_ceo SET image_id=%s, name=%s, detail=%s, user_id=%s, status=%s, created_at=%s, updated_at=%s
        WHERE id=%s
    """, (
        data.get("image_id"),
        data.get("name"),
        data.get("detail"),
        data.get("user_id"),
        data.get("status", 1),
        created_at,
        updated_at,
        ceo_id
    ))

    conn.commit()
    conn.close()
    return {"id": ceo_id, **data, "created_at": created_at, "updated_at": updated_at}

def delete_ceo(ceo_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE profile_ceo SET status = 0 WHERE id = %s", (ceo_id,))
    conn.commit()
    conn.close()
    return {"message": f"Profile CEO {ceo_id} soft-deleted (status = 0)"}
