import datetime
from db import get_db_connection

def assign_permissions_to_user(user_id: int, permission_ids: list):
    """
    Assign multiple permissions to a user using role_permission_id mapping.
    """
    if not permission_ids:
        return {"error": "No permission_ids provided"}

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get existing role_permission IDs
    cursor.execute(
        "SELECT id FROM role_permission WHERE permission_id IN (%s)" % 
        ",".join(["%s"]*len(permission_ids)), tuple(permission_ids)
    )
    role_permission_rows = cursor.fetchall()
    if not role_permission_rows:
        conn.close()
        return {"error": "No matching role_permission found"}

    role_permission_ids = [row["id"] for row in role_permission_rows]

    # Get already assigned to user
    cursor.execute(
        "SELECT permission_id FROM user_permission WHERE user_id=%s AND status=1", 
        (user_id,)
    )
    existing = {row["permission_id"] for row in cursor.fetchall()}

    now = datetime.datetime.now()
    assigned = []
    for rp_id in role_permission_ids:
        if rp_id not in existing:
            cursor.execute(
                "INSERT INTO user_permission (user_id, permission_id, status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)",
                (user_id, rp_id, 1, now, now)
            )
            assigned.append(rp_id)

    conn.commit()
    conn.close()

    return {"user_id": user_id, "assigned_permission_ids": assigned, "skipped": list(existing & set(role_permission_ids))}
