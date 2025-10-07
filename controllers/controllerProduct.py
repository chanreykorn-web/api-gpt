import datetime
from db import get_db_connection

def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Join product with product_spicification and product_images
    cursor.execute("""
        SELECT 
            p.id AS product_id,
            p.name AS product_name,
            p.detail,
            p.status,
            p.created_at,
            p.updated_at,
            p.category_id,
            p.image_id,
            p.path AS primary_path,
            p.user_id,
            ps.spicification_id,
            pi.id AS product_image_id,
            pi.image_path
        FROM product p
        LEFT JOIN product_spicification ps ON ps.product_id = p.id
        LEFT JOIN product_images pi ON pi.product_id = p.id
        WHERE p.status = 1
        ORDER BY p.id
    """)

    rows = cursor.fetchall()
    conn.close()

    products = {}
    for row in rows:
        pid = row["product_id"]
        if pid not in products:
            products[pid] = {
                "id": pid,
                "name": row["product_name"],
                "detail": row["detail"],
                "status": row["status"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "category_id": row["category_id"],
                "image_id": row["image_id"],
                "primary_path": row["primary_path"],
                "user_id": row["user_id"],
                "spicifications": [],
                "images": []   # 🔹 store multiple images here
            }

        # Add specification if exists
        if row["spicification_id"] and row["spicification_id"] not in products[pid]["spicifications"]:
            products[pid]["spicifications"].append(row["spicification_id"])

        # Add image if exists
        if row["product_image_id"]:
            img_obj = {
                "id": row["product_image_id"],
                "path": row["image_path"]
            }
            if img_obj not in products[pid]["images"]:
                products[pid]["images"].append(img_obj)

    return list(products.values())



def get_product_by_id(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Join product with product_spicification and product_images
    cursor.execute("""
        SELECT 
            p.id AS product_id,
            p.name AS product_name,
            p.detail,
            p.status,
            p.created_at,
            p.updated_at,
            p.category_id,
            p.image_id,
            p.path AS primary_path,
            p.user_id,
            ps.spicification_id,
            pi.id AS product_image_id,
            pi.image_path
        FROM product p
        LEFT JOIN product_spicification ps ON ps.product_id = p.id
        LEFT JOIN product_images pi ON pi.product_id = p.id
        WHERE p.id = %s
    """, (product_id,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return None

    product = {
        "id": rows[0]["product_id"],
        "name": rows[0]["product_name"],
        "detail": rows[0]["detail"],
        "status": rows[0]["status"],
        "created_at": rows[0]["created_at"],
        "updated_at": rows[0]["updated_at"],
        "category_id": rows[0]["category_id"],
        "image_id": rows[0]["image_id"],
        "primary_path": rows[0]["primary_path"],
        "user_id": rows[0]["user_id"],
        "spicifications": [],
        "images": []
    }

    for row in rows:
        # Add specification
        if row["spicification_id"] and row["spicification_id"] not in product["spicifications"]:
            product["spicifications"].append(row["spicification_id"])
        # Add image
        if row["product_image_id"]:
            img_obj = {
                "id": row["product_image_id"],
                "path": row["image_path"]
            }
            if img_obj not in product["images"]:
                product["images"].append(img_obj)

    return product




def create_product(data: dict):
    """
    Create a new product with:
    - category_id, title, description, category_sub, category, user_id, status
    - multiple specifications
    - multiple images
    - first image stored as product.image_id / product.path
    """

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    now = datetime.datetime.now()

    try:
        # Ensure images is a list of dicts with id and path
        images = data.get("images", [])
        images = [img for img in images if img.get("id") and img.get("path")]
        first_image = images[0] if images else None

        # Insert main product
        cursor.execute("""
    INSERT INTO product 
    (category, category_sub, name, image_id, path, detail, user_id, category_id, status, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (
    data.get("category"),
    data.get("category_sub"),
    data.get("name"),  # or name, depending on payload
    first_image['id'] if first_image else None,
    first_image['path'] if first_image else None,   # ✅ primary image path
    data.get("detail"),                        # ✅ detail/description
    data.get("user_id"),
    data.get("category_id"),                        # ✅ proper FK
    data.get("status", 1),
    now,
    now
))


        product_id = cursor.lastrowid

        # Insert multiple specifications
        spic_ids = data.get("spicification_id", [])
        if isinstance(spic_ids, list):
            for spic_id in spic_ids:
                cursor.execute("""
                    INSERT INTO product_spicification (product_id, spicification_id)
                    VALUES (%s, %s)
                """, (product_id, spic_id))

        # Insert multiple images
        for img in images:
            cursor.execute("""
                INSERT INTO product_images (product_id, image_path, created_at, updated_at)
                VALUES (%s, %s, %s, %s)
            """, (product_id, img['path'], now, now))

        conn.commit()

        return {
    "id": product_id,
    "name": data.get("name"),
    "detail": data.get("detail"),
    "status": data.get("status", 1),
    "created_at": now,
    "updated_at": now,
    "category_id": data.get("category_id"),
    "image_id": first_image['id'] if first_image else None,
    "primary_path": first_image['path'] if first_image else None,   # ✅ correct path
    "user_id": data.get("user_id"),
    "spicifications": spic_ids,
    "images": images
}


    except Exception as e:
        conn.rollback()
        print("Insert error:", e)
        return {"error": str(e)}
    finally:
        conn.close()

def update_product(product_id: int, data: dict):
    """
    Update a product with:
    - Basic fields: category, category_sub, name, detail, status, etc.
    - Multiple specifications
    - Multiple images (new and existing)
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1️⃣ Fetch existing created_at
        cursor.execute("SELECT created_at FROM product WHERE id = %s", (product_id,))
        row = cursor.fetchone()
        if not row:
            return { "error": "Product not found" }

        created_at = row["created_at"]
        updated_at = datetime.datetime.now()

        # 2️⃣ Determine primary image (first image in list)
        images = data.get("images", [])
        first_image = images[0] if images else None

        # 3️⃣ Update main product table
        cursor.execute("""
            UPDATE product SET
                category = %s,
                category_sub = %s,
                name = %s,
                image_id = %s,
                path = %s,
                detail = %s,
                detail_product = %s,
                detail_path = %s,
                user_id = %s,
                category_id = %s,
                status = %s,
                created_at = %s,
                updated_at = %s
            WHERE id = %s
        """, (
            data.get("category"),
            data.get("category_sub"),
            data.get("name"),
            first_image['id'] if first_image else None,
            first_image['path'] if first_image else None,
            data.get("detail"),
            data.get("detail_product"),
            data.get("detail_path"),
            data.get("user_id"),
            data.get("category_id"),
            data.get("status", 1),
            created_at,
            updated_at,
            product_id
        ))

        # 4️⃣ Update specifications
        # Delete old ones
        cursor.execute("DELETE FROM product_spicification WHERE product_id = %s", (product_id,))
        spic_ids = data.get("spicification_id", [])
        for spic_id in spic_ids:
            cursor.execute("""
                INSERT INTO product_spicification (product_id, spicification_id)
                VALUES (%s, %s)
            """, (product_id, spic_id))

        # 5️⃣ Update images
        # Optional: remove old images if needed
        cursor.execute("DELETE FROM product_images WHERE product_id = %s", (product_id,))
        for img in images:
            cursor.execute("""
                INSERT INTO product_images (product_id, image_path, created_at, updated_at)
                VALUES (%s, %s, %s, %s)
            """, (product_id, img['path'], updated_at, updated_at))

        conn.commit()
        return { "id": product_id, **data }

    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close()

def delete_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE product SET status = 0 WHERE id = %s", (product_id,))
    conn.commit()
    conn.close()
    return { "message": f"Product {product_id} soft-deleted" }


def get_all_products_public():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            p.id AS product_id,
            p.name AS product_name,
            p.detail,
            p.status,
            p.created_at,
            p.updated_at,
            p.category_id,
            p.image_id,
            p.path AS primary_path,
            p.user_id,

            ps.spicification_id,
            s.title AS spec_title,
            s.descriptions AS spec_description,

            pi.id AS product_image_id,
            pi.image_path
        FROM product p
        LEFT JOIN product_spicification ps ON ps.product_id = p.id
        LEFT JOIN spicification s ON s.id = ps.spicification_id
        LEFT JOIN product_images pi ON pi.product_id = p.id
        WHERE p.status = 1
        ORDER BY p.id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    products = {}
    for row in rows:
        pid = row["product_id"]
        if pid not in products:
            products[pid] = {
                "id": pid,
                "name": row["product_name"],
                "detail": row["detail"],
                "status": row["status"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "category_id": row["category_id"],
                "image_id": row["image_id"],
                "primary_path": row["primary_path"],
                "user_id": row["user_id"],
                "spicifications": [],
                "images": []
            }

        # ✅ Add specification
        if row["spicification_id"]:
            spec_obj = {
                "id": row["spicification_id"],
                "title": row.get("spec_title"),
                "description": row.get("spec_description")
            }
            if spec_obj not in products[pid]["spicifications"]:
                products[pid]["spicifications"].append(spec_obj)

        # ✅ Add image
        if row["product_image_id"]:
            img_obj = {
                "id": row["product_image_id"],
                "path": row["image_path"]
            }
            if img_obj not in products[pid]["images"]:
                products[pid]["images"].append(img_obj)

    # ✅ Return as list
    return list(products.values())

def get_product_by_id(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            p.id AS product_id,
            p.name AS product_name,
            p.detail,
            p.status,
            p.created_at,
            p.updated_at,
            p.category_id,
            p.image_id,
            p.path AS primary_path,
            p.user_id,

            ps.spicification_id,
            s.title AS spec_title,
            s.descriptions AS spec_description,

            pi.id AS product_image_id,
            pi.image_path
        FROM product p
        LEFT JOIN product_spicification ps ON ps.product_id = p.id
        LEFT JOIN spicification s ON s.id = ps.spicification_id
        LEFT JOIN product_images pi ON pi.product_id = p.id
        WHERE p.status = 1 AND p.id = %s
    """, (product_id,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return None  # Product not found

    # Initialize product object
    row = rows[0]
    product = {
        "id": row["product_id"],
        "name": row["product_name"],
        "detail": row["detail"],
        "status": row["status"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "category_id": row["category_id"],
        "image_id": row["image_id"],
        "primary_path": row["primary_path"],
        "user_id": row["user_id"],
        "spicifications": [],
        "images": []
    }

    # Collect specifications and images
    for row in rows:
        if row["spicification_id"]:
            spec_obj = {
                "id": row["spicification_id"],
                "title": row.get("spec_title"),
                "description": row.get("spec_description")
            }
            if spec_obj not in product["spicifications"]:
                product["spicifications"].append(spec_obj)

        if row["product_image_id"]:
            img_obj = {
                "id": row["product_image_id"],
                "path": row["image_path"]
            }
            if img_obj not in product["images"]:
                product["images"].append(img_obj)

    return product


def get_all_products_by_category_public(category: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            p.id AS product_id,
            p.name AS product_name,
            p.detail,
            p.status,
            p.created_at,
            p.updated_at,
            p.category_id,
            p.image_id,
            p.path AS primary_path,
            p.user_id,
            
            ps.spicification_id,
            s.descriptions AS spec_name,
            s.descriptions AS spec_value,   -- if your table has it

            pi.id AS product_image_id,
            pi.image_path
        FROM product p
        LEFT JOIN product_spicification ps ON ps.product_id = p.id
        LEFT JOIN spicification s ON s.id = ps.spicification_id   -- ✅ join to fetch spec details
        LEFT JOIN product_images pi ON pi.product_id = p.id
        WHERE p.status = 1
          AND p.category_id = %s
        ORDER BY p.id
    """, (category,))

    rows = cursor.fetchall()
    conn.close()

    products = {}
    for row in rows:
        pid = row["product_id"]
        if pid not in products:
            products[pid] = {
                "id": pid,
                "name": row["product_name"],
                "detail": row["detail"],
                "status": row["status"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "category_id": row["category_id"],
                "image_id": row["image_id"],
                "primary_path": row["primary_path"],
                "user_id": row["user_id"],
                "spicifications": [],
                "images": []
            }

        # ✅ Add full specification object
        if row["spicification_id"]:
            spec_obj = {
                "id": row["spicification_id"],
                "title": row.get("spec_name"),
                "descriptions": row.get("spec_value")
            }
            if spec_obj not in products[pid]["spicifications"]:
                products[pid]["spicifications"].append(spec_obj)

        # ✅ Add image
        if row["product_image_id"]:
            img_obj = {
                "id": row["product_image_id"],
                "path": row["image_path"]
            }
            if img_obj not in products[pid]["images"]:
                products[pid]["images"].append(img_obj)

    return list(products.values())


def get_all_new_products_public():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            p.id AS product_id,
            p.name AS product_name,
            p.detail,
            p.status,
            p.new,                   -- new field
            p.created_at,
            p.updated_at,
            p.category_id,
            p.image_id,
            p.path AS primary_path,
            p.user_id,

            ps.spicification_id,
            s.title AS spec_title,
            s.descriptions AS spec_description,

            pi.id AS product_image_id,
            pi.image_path
        FROM product p
        LEFT JOIN product_spicification ps ON ps.product_id = p.id
        LEFT JOIN spicification s ON s.id = ps.spicification_id
        LEFT JOIN product_images pi ON pi.product_id = p.id
        WHERE p.status = 1 AND p.new = 1
        ORDER BY p.id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    products = {}
    for row in rows:
        pid = row["product_id"]
        if pid not in products:
            products[pid] = {
                "id": pid,
                "name": row["product_name"],
                "detail": row["detail"],
                "status": row["status"],
                "new": row["new"],             # include new field
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "category_id": row["category_id"],
                "image_id": row["image_id"],
                "primary_path": row["primary_path"],
                "user_id": row["user_id"],
                "spicifications": [],
                "images": []
            }

        # Add specification
        if row["spicification_id"]:
            spec_obj = {
                "id": row["spicification_id"],
                "title": row.get("spec_title"),
                "description": row.get("spec_description")
            }
            if spec_obj not in products[pid]["spicifications"]:
                products[pid]["spicifications"].append(spec_obj)

        # Add image
        if row["product_image_id"]:
            img_obj = {
                "id": row["product_image_id"],
                "path": row["image_path"]
            }
            if img_obj not in products[pid]["images"]:
                products[pid]["images"].append(img_obj)

    return list(products.values())


def update_product_category(product_id: int, data: dict):
    """
    Update only the product_category field for a product.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # ✅ Check if product exists
        cursor.execute("SELECT id FROM product WHERE id = %s", (product_id,))
        row = cursor.fetchone()
        if not row:
            return {"error": "Product not found"}

        # ✅ Update only product_category
        cursor.execute("""
            UPDATE product 
            SET product_category = %s,
                updated_at = %s
            WHERE id = %s
        """, (
            data.get("product_category"),
            datetime.datetime.now(),
            product_id
        ))

        conn.commit()
        return {"id": product_id, "product_category": data.get("product_category")}

    except Exception as e:
        conn.rollback()
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()

def update_product_new(product_id: int, data: dict):
    """
    Update only the 'new' field for a product.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # ✅ Check if product exists
        cursor.execute("SELECT id FROM product WHERE id = %s", (product_id,))
        row = cursor.fetchone()
        if not row:
            return {"success": False, "error": "Product not found"}

        # ✅ Update only 'new' field
        cursor.execute("""
            UPDATE product 
            SET new = %s,
                updated_at = %s
            WHERE id = %s
        """, (
            data.get("new"),
            datetime.datetime.utcnow(),  # use UTC for consistency
            product_id
        ))

        conn.commit()
        return {"success": True, "id": product_id, "new": data.get("new")}

    except Exception as e:
        conn.rollback()
        return {"success": False, "error": str(e)}

    finally:
        cursor.close()
        conn.close()