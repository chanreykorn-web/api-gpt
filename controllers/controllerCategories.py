import datetime
from db import get_db_connection

def get_all_categories():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get all active categories
    cursor.execute("SELECT * FROM category WHERE status = 1")
    categories = cursor.fetchall()

    # For each category, fetch images
    for category in categories:
        cursor.execute("SELECT id, image_id, path FROM category_images WHERE category_id = %s", (category["id"],))
        category["images"] = cursor.fetchall()

    conn.close()
    return categories


def get_category_by_id(category_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get main category
    cursor.execute("SELECT * FROM category WHERE id = %s", (category_id,))
    category = cursor.fetchone()

    if category:
        # Get related images
        cursor.execute("SELECT id, image_id, path FROM category_images WHERE category_id = %s", (category_id,))
        category["images"] = cursor.fetchall()
    else:
        category = None

    conn.close()
    return category


def create_category(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()

    # pick the first image from the list (if any) as cover
    images = data.get("images", [])
    first_image = images[0] if images else None

    # 1. Insert into category (main table)
    cursor.execute("""
        INSERT INTO category
            (name, image_id, path, discriptions, user_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("name"),
        first_image["id"] if first_image else None,   # cover image id
        first_image["path"] if first_image else None, # cover image path
        data.get("discriptions"),
        data.get("user_id"),
        data.get("status", 1),
        now,
        now
    ))

    category_id = cursor.lastrowid

    # 2. Insert multiple images into category_images
    for img in images:
        cursor.execute("""
            INSERT INTO category_images (category_id, image_id, path, created_at)
            VALUES (%s, %s, %s, %s)
        """, (
            category_id,
            img.get("id"),
            img.get("path"),
            now
        ))

    conn.commit()
    conn.close()

    return {
        "id": category_id,
        "name": data.get("name"),
        "image_id": first_image["id"] if first_image else None,
        "path": first_image["path"] if first_image else None,
        "discriptions": data.get("discriptions"),
        "status": data.get("status", 1),
        "user_id": data.get("user_id"),
        "images": images
    }



def update_category(category_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Preserve created_at
    cursor.execute("SELECT created_at FROM category WHERE id = %s", (category_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"error": "Category not found"}

    created_at = row["created_at"]
    updated_at = datetime.datetime.now()
    
    # === Update category main table ===
    cursor.execute("""
        UPDATE category
        SET name = %s, image_id = %s, path = %s, user_id = %s, discriptions = %s, status = %s, created_at = %s, updated_at = %s
        WHERE id = %s
    """, (
        data.get("name"),
        data.get("image_id"),
        data.get("path"),
        data.get("user_id"),
        data.get("discriptions"),
        data.get("status", 1),
        created_at,
        updated_at,
        category_id
    ))

    # === Manage multi-images ===
    if "images" in data:
        # Delete old images
        cursor.execute("DELETE FROM category_images WHERE category_id = %s", (category_id,))

        # Insert new ones (without updated_at)
        for img in data["images"]:
            cursor.execute("""
                INSERT INTO category_images (category_id, image_id, path, created_at)
                VALUES (%s, %s, %s, %s)
            """, (
                category_id,
                img.get("id"),
                img.get("path"),
                created_at
            ))

    conn.commit()
    conn.close()

    return {
        "id": category_id,
        **data,
        "created_at": created_at,
        "updated_at": updated_at
    }

def delete_category(category_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE category SET status = 0 WHERE id = %s", (category_id,))
    conn.commit()
    conn.close()
    return { "message": f"Category {category_id} soft-deleted (status = 0)" }


def get_all_categories_public():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get all active categories
    cursor.execute("SELECT * FROM category WHERE status = 1")
    categories = cursor.fetchall()

    # For each category, fetch images
    for category in categories:
        cursor.execute("SELECT id, image_id, path FROM category_images WHERE category_id = %s", (category["id"],))
        category["images"] = cursor.fetchall()

    conn.close()
    return categories