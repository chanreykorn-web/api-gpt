import datetime
from db import get_db_connection

def get_all_permissions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM permission WHERE status = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_permission_by_id(permission_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM permission WHERE id = %s", (permission_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_permission(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()
    cursor.execute("""
        INSERT INTO permission (name, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s)
    """, (
        data.get("name"),
        data.get("status", 1),
        now,
        now
    ))
    conn.commit()
    permission_id = cursor.lastrowid
    conn.close()
    return { "id": permission_id, **data }

def update_permission(permission_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT created_at FROM permission WHERE id = %s", (permission_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return { "error": "Permission not found" }

    created_at = row["created_at"]
    updated_at = datetime.datetime.now()

    cursor.execute("""
        UPDATE permission SET name = %s, status = %s, created_at = %s, updated_at = %s WHERE id = %s
    """, (
        data.get("name"),
        data.get("status", 1),
        created_at,
        updated_at,
        permission_id
    ))

    conn.commit()
    conn.close()
    return { "id": permission_id, **data }

def delete_permission(permission_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE permission SET status = 0 WHERE id = %s", (permission_id,))
    conn.commit()
    conn.close()
    return { "message": f"Permission {permission_id} soft-deleted" }
