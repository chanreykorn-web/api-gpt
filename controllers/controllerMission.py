import datetime
from db import get_db_connection


def get_all_missions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mission WHERE status = 1")
    missions = cursor.fetchall()
    conn.close()
    return missions

def get_mission_by_id(mission_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mission WHERE id = %s AND status = 1", (mission_id,))
    mission = cursor.fetchone()
    conn.close()
    return mission

def create_mission(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()

    query = """
        INSERT INTO mission (mission, value, history, image_id, path, user_id, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data.get("mission"),
        data.get("value"),
        data.get("history"),
        data.get("image_id"),
        data.get("path"),
        data.get("user_id"),
        data.get("status", 1),
        now,
        now
    )
    cursor.execute(query, values)
    conn.commit()
    mission_id = cursor.lastrowid
    conn.close()
    return { "id": mission_id, **data }


def update_mission(mission_id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()

    query = """
        UPDATE mission SET mission = %s, value = %s, history = %s, image_id = %s, path = %s, user_id = %s, status = %s, updated_at = %s
        WHERE id = %s
    """
    values = (
        data.get("mission"),
        data.get("value"),
        data.get("history"),
        data.get("image_id"),
        data.get("path"),
        data.get("user_id"),
        data.get("status", 1),
        now,
        mission_id
    )
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return { "id": mission_id, **data }


def delete_mission(mission_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE mission SET status = 0 WHERE id = %s", (mission_id,))
    conn.commit()
    conn.close()
    return { "message": "Mission soft-deleted" }


def get_all_missions_public():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mission WHERE status = 1")
    missions = cursor.fetchall()
    conn.close()
    return missions