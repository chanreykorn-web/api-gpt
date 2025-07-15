import datetime
from db import get_db_connection

def get_all_form_contacts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM form_contact")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_form_contact_by_id(contact_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM form_contact WHERE id = %s", (contact_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_form_contact(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()
    cursor.execute("""
        INSERT INTO form_contact (title, name, subject, email, message, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data.get("title"),
        data.get("name"),
        data.get("subject"),
        data.get("email"),
        data.get("message"),
        now
    ))
    conn.commit()
    contact_id = cursor.lastrowid
    conn.close()
    return { "id": contact_id, **data, "created_at": now }

def update_form_contact(contact_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get original created_at to preserve
    cursor.execute("SELECT created_at FROM form_contact WHERE id = %s", (contact_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return { "error": "Form contact not found" }

    created_at = row[0]
    cursor.execute("""
        UPDATE form_contact SET title = %s, name = %s, subject = %s, email = %s, message = %s, created_at = %s
        WHERE id = %s
    """, (
        data.get("title"),
        data.get("name"),
        data.get("subject"),
        data.get("email"),
        data.get("message"),
        created_at,
        contact_id
    ))
    conn.commit()
    conn.close()
    return { "id": contact_id, **data, "created_at": created_at }

def delete_form_contact(contact_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM form_contact WHERE id = %s", (contact_id,))
    conn.commit()
    conn.close()
    return { "message": f"Form contact {contact_id} deleted" }
