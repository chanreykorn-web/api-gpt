from db import get_db_connection

def get_all_contacts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contact_us")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_contact_by_id(contact_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contact_us WHERE id = %s", (contact_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_contact(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contact_us (title, email, telegram, facebook, instagram, tiktok, youtube, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("title"),
        data.get("email"),
        data.get("telegram"),
        data.get("facebook"),
        data.get("instagram"),
        data.get("tiktok"),
        data.get("youtube"),
        data.get("address")
    ))
    conn.commit()
    contact_id = cursor.lastrowid
    conn.close()
    return { "id": contact_id, **data }

def update_contact(contact_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE contact_us SET
        title = %s, email = %s, telegram = %s, facebook = %s,
        instagram = %s, tiktok = %s, youtube = %s, address = %s
        WHERE id = %s
    """, (
        data.get("title"),
        data.get("email"),
        data.get("telegram"),
        data.get("facebook"),
        data.get("instagram"),
        data.get("tiktok"),
        data.get("youtube"),
        data.get("address"),
        contact_id
    ))
    conn.commit()
    conn.close()
    return { "id": contact_id, **data }

def delete_contact(contact_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contact_us WHERE id = %s", (contact_id,))
    conn.commit()
    conn.close()
    return { "message": f"Contact {contact_id} deleted" }
