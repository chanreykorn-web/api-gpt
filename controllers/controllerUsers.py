from db import get_db_connection
from auth import hash_password
import datetime

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_user_by_id(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_user(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()

    # ✅ Hash the password before inserting
    hashed_password = hash_password(data.get("password")) 

    query = """
        INSERT INTO users 
        (username, password, email, role_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data.get("username"),
        hashed_password,
        data.get("email"),
        data.get("role_id"),
        data.get("status", 1),
        now,
        now
    )

    cursor.execute(query, values)
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return { "id": user_id, **data, "password": "hashed" }  # optionally hide real password in response

def update_user(user_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()

    # Get existing user (to preserve old password if not updating it)
    cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
    existing = cursor.fetchone()
    if not existing:
        conn.close()
        return {"error": "User not found"}

    # ✅ Check if password is being updated
    raw_password = data.get("password")
    if raw_password:
        hashed_password = hash_password(raw_password)
    else:
        hashed_password = existing[0]  # Keep existing hashed password

    query = """
        UPDATE users SET
        username=%s, password=%s, email=%s, role_id=%s, status=%s, updated_at=%s
        WHERE id = %s
    """
    values = (
        data.get("username"),
        hashed_password,
        data.get("email"),
        data.get("role_id"),
        data.get("status", 1),
        now,
        user_id
    )

    cursor.execute(query, values)
    conn.commit()
    conn.close()

    # Optional: mask password in return
    return {"id": user_id, **data, "password": "updated (if provided)"}

def delete_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "UPDATE users SET status = 1 WHERE id = %s"
    cursor.execute(query, (user_id,))
    conn.commit()
    conn.close()

    return {"message": f"User {user_id} user delete success!"}
