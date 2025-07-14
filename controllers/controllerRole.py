import datetime
from db import get_db_connection


def get_all_roles():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM role WHERE status = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_role_by_id(role_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM role WHERE id = %s", (role_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_role(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if name exists
    cursor.execute("SELECT * FROM role WHERE name = %s AND status = 1", (data.get("name"),))
    if cursor.fetchone():
        conn.close()
        return {"error": "Role name already exists"}

    now = datetime.datetime.now()
    cursor.execute("""
        INSERT INTO role (name, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s)
    """, (data.get("name"), data.get("status", 1), now, now))

    conn.commit()
    role_id = cursor.lastrowid
    conn.close()
    return {"id": role_id, **data}


def update_role(role_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ 1. Prevent duplicate name
    cursor.execute("SELECT * FROM role WHERE name = %s AND id != %s AND status = 1", (data.get("name"), role_id))
    if cursor.fetchone():
        conn.close()
        return {"error": "Role name already exists"}

    # ✅ 2. Fetch existing created_at
    cursor.execute("SELECT created_at FROM role WHERE id = %s", (role_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"error": "Role not found"}

    created_at = row["created_at"]
    updated_at = datetime.datetime.now()

    # ✅ 3. Update role (preserve created_at)
    cursor.execute("""
        UPDATE role 
        SET name = %s, status = %s, created_at = %s, updated_at = %s 
        WHERE id = %s
    """, (
        data.get("name"),
        data.get("status", 1),
        created_at,
        updated_at,
        role_id
    ))

    conn.commit()
    conn.close()

    return {
        "id": role_id,
        "name": data.get("name"),
        "status": data.get("status", 1),
        "created_at": created_at,
        "updated_at": updated_at
    }


def delete_role(role_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Soft delete (status = 0)
    cursor.execute("UPDATE role SET status = 1 WHERE id = %s", (role_id,))
    conn.commit()
    conn.close()

    return {"message": f"Role {role_id} deleted success!"}