import datetime
from db import get_db_connection

def get_all_solutions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM solution WHERE status = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_solution_by_id(solution_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM solution WHERE id = %s", (solution_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_solution(data: dict):
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
        INSERT INTO solution (category, category_sub, title, image_id, path, user_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("category"),
        data.get("category_sub"),
        data.get("title"),
        data.get("image_id"),
        data.get("path"),
        data.get("user_id"),
        data.get("status", 1),
        now,
        now
    ))

    conn.commit()
    solution_id = cursor.lastrowid
    conn.close()
    return { "id": solution_id, **data }

def update_solution(solution_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get current created_at to preserve
    cursor.execute("SELECT created_at FROM solution WHERE id = %s", (solution_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return { "error": "Solution not found" }

    created_at = row["created_at"]
    updated_at = datetime.datetime.now()

    cursor.execute("""
        UPDATE solution SET
        category = %s,
        category_sub = %s,
        title = %s,
        image_id = %s,
        path = %s,
        user_id = %s,
        status = %s,
        created_at = %s,
        updated_at = %s
        WHERE id = %s
    """, (
        data.get("category"),
        data.get("category_sub"),
        data.get("title"),
        data.get("image_id"),
        data.get("path"),
        data.get("user_id"),
        data.get("status", 1),
        created_at,
        updated_at,
        solution_id
    ))

    conn.commit()
    conn.close()
    return { "id": solution_id, **data }

def delete_solution(solution_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE solution SET status = 0 WHERE id = %s", (solution_id,))
    conn.commit()
    conn.close()
    return { "message": f"Solution {solution_id} soft-deleted" }


def get_all_solutions_public():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get last 4 inserted rows where status = 1
    cursor.execute("""
        SELECT * 
        FROM solution 
        WHERE status = 1 
        ORDER BY id DESC 
        LIMIT 4
    """)
    
    rows = cursor.fetchall()
    conn.close()
    return rows



def get_solution_public_by_id(solution_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM solution WHERE id = %s", (solution_id,))
    row = cursor.fetchone()
    conn.close()
    return row
