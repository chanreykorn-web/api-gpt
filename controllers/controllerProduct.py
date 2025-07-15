import datetime
from db import get_db_connection

def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM product WHERE status = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_product_by_id(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM product WHERE id = %s", (product_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_product(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()

    cursor.execute("""
        INSERT INTO product (name, image_id, detail, user_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("name"),
        data.get("image_id"),
        data.get("detail"),
        data.get("user_id"),
        data.get("status", 1),
        now,
        now
    ))

    conn.commit()
    product_id = cursor.lastrowid
    conn.close()

    return { "id": product_id, **data }

def update_product(product_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Preserve created_at
    cursor.execute("SELECT created_at FROM product WHERE id = %s", (product_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return { "error": "Product not found" }

    created_at = row["created_at"]
    updated_at = datetime.datetime.now()

    cursor.execute("""
        UPDATE product
        SET name = %s, image_id = %s, detail = %s, user_id = %s,
            status = %s, created_at = %s, updated_at = %s
        WHERE id = %s
    """, (
        data.get("name"),
        data.get("image_id"),
        data.get("detail"),
        data.get("user_id"),
        data.get("status", 1),
        created_at,
        updated_at,
        product_id
    ))

    conn.commit()
    conn.close()

    return { "id": product_id, **data, "created_at": created_at, "updated_at": updated_at }

def delete_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE product SET status = 0 WHERE id = %s", (product_id,))
    conn.commit()
    conn.close()
    return { "message": f"Product {product_id} soft-deleted (status = 0)" }
