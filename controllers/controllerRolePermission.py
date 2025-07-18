import datetime
from db import get_db_connection

def get_all_role_permissions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM role_permission WHERE status = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_role_permission_by_id(role_permission_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM role_permission WHERE id = %s", (role_permission_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_role_permission(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check role
    cursor.execute("SELECT id FROM role WHERE id = %s", (data.get("role_id"),))
    if not cursor.fetchone():
        conn.close()
        return { "error": "role_id not found" }

    # Check permission
    cursor.execute("SELECT id FROM permission WHERE id = %s", (data.get("permission_id"),))
    if not cursor.fetchone():
        conn.close()
        return { "error": "permission_id not found" }

    now = datetime.datetime.now()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO role_permission (role_id, permission_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data.get("role_id"),
        data.get("permission_id"),
        data.get("status", 1),
        now,
        now
    ))

    conn.commit()
    role_permission_id = cursor.lastrowid
    conn.close()
    return { "id": role_permission_id, **data }

def update_role_permission(role_permission_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT created_at FROM role_permission WHERE id = %s", (role_permission_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return { "error": "Role permission not found" }

    created_at = row["created_at"]
    updated_at = datetime.datetime.now()

    cursor.execute("""
        UPDATE role_permission
        SET role_id = %s, permission_id = %s, status = %s, created_at = %s, updated_at = %s
        WHERE id = %s
    """, (
        data.get("role_id"),
        data.get("permission_id"),
        data.get("status", 1),
        created_at,
        updated_at,
        role_permission_id
    ))

    conn.commit()
    conn.close()
    return { "id": role_permission_id, **data }

def delete_role_permission(role_permission_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE role_permission SET status = 0 WHERE id = %s", (role_permission_id,))
    conn.commit()
    conn.close()
    return { "message": f"RolePermission {role_permission_id} soft-deleted" }
