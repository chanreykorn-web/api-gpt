import email
from fastapi import HTTPException
from db import get_db_connection
from security import hash_password
from security import hash_password, verify_password
import datetime

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def get_user_by_id(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def create_user(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO users (username, password, email, role_id, status, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    now = datetime.datetime.now()
    hashed_pw = hash_password(data['password'])
    cursor.execute(sql, (
        data['username'],
        hashed_pw,
        data['email'],
        data.get('role_id'),
        data.get('status', 1),
        now,
        now
    ))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id}

def authenticate_user(email: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return user

def update_user(user_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
    UPDATE users
    SET username=%s, email=%s, role_id=%s, status=%s, updated_at=%s
    WHERE id = %s
    """
    cursor.execute(sql, (
        data['username'],
        data.get('email'),  # fixed here
        data.get('role_id'),
        data['status'],
        datetime.datetime.now(),
        user_id
    ))
    conn.commit()
    conn.close()
    return {"message": "User updated successfully"}

def delete_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
    UPDATE users
    SET status = 0
    WHERE id = %s
    """
    cursor.execute(sql, (user_id,))
    conn.commit()
    conn.close()
    return {"message": "User deactivated (status=0)"}


def get_permissions_for_role(role_id: int) -> list[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.name
        FROM permissions p
        JOIN role_permissions rp ON p.id = rp.permission_id
        WHERE rp.role_id = %s
    """, (role_id,))
    perms = [row[0] for row in cursor.fetchall()]
    conn.close()
    return perms


from db import get_db_connection

def get_user_from_db(email: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT u.id, u.email, u.password, r.name AS role
        FROM users u
        JOIN role r ON u.role_id = r.id
        WHERE u.email = %s
    """
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def get_user_permissions(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Permissions from role
    sql_role = """
        SELECT p.name AS permission
        FROM permission p
        JOIN role_permission rp ON rp.permission_id = p.id
        JOIN users u ON u.role_id = rp.role_id
        WHERE u.id = %s
    """
    cursor.execute(sql_role, (user_id,))
    role_permissions = [row['permission'] for row in cursor.fetchall()]

    # Permissions assigned directly to user
    sql_user = """
        SELECT p.name AS permission
        FROM permission p
        JOIN user_permission up ON up.permission_id = p.id
        WHERE up.user_id = %s
    """
    cursor.execute(sql_user, (user_id,))
    user_permissions = [row['permission'] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    # Merge and remove duplicates
    return list(set(role_permissions + user_permissions))
