import os
import shutil
import datetime
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from db import get_db_connection  # Must be synchronous

# router = APIRouter()

router = APIRouter(prefix="/api/gallery", tags=["Gallery"])

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def create_gallery(
    file: UploadFile,
    user_id: int,
    image_id: Optional[int] = None
):
    """
    Upload single image and insert into gallery table
    """

    try:
        conn = get_db_connection()  # Synchronous
        cursor = conn.cursor()

        # Save file
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Insert DB record
        now = datetime.datetime.now()
        cursor.execute(
            """
            INSERT INTO gallery (path, image_id, user_id, status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (filename, image_id, user_id, 1, now, now)
        )

        conn.commit()
        return {"message": "Upload successful", "file": filename}

    except Exception as e:
        if conn:
            conn.rollback()
        return JSONResponse(status_code=500, content={"error": str(e)})

    finally:
        if conn:
            conn.close()


# ----------------------------
# GET ALL ACTIVE GALLERY ITEMS
# ----------------------------
@router.get("/gallery")
def get_all_gallery():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gallery WHERE status = 1")
    rows = cursor.fetchall()
    conn.close()
    return {"gallery": rows}


# ----------------------------
# GET GALLERY BY ID
# ----------------------------
@router.get("/gallery/{gallery_id}")
def get_gallery_by_id(gallery_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gallery WHERE id = %s", (gallery_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"gallery": row}
    return JSONResponse(status_code=404, content={"error": "Gallery not found"})


# ----------------------------
# UPDATE GALLERY
# ----------------------------
@router.put("/gallery/{gallery_id}")
def update_gallery(gallery_id: int, image_id: int = Form(None), user_id: int = Form(None), status: int = Form(1)):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()

    try:
        cursor.execute(
            """
            UPDATE gallery
            SET image_id = %s, user_id = %s, status = %s, updated_at = %s
            WHERE id = %s
            """,
            (image_id, user_id, status, now, gallery_id)
        )
        conn.commit()
        return {"message": "Gallery updated", "id": gallery_id}

    except Exception as e:
        conn.rollback()
        return JSONResponse(status_code=500, content={"error": str(e)})

    finally:
        conn.close()


# ----------------------------
# SOFT DELETE GALLERY
# ----------------------------
@router.delete("/gallery/{gallery_id}")
def delete_gallery(gallery_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # So we can fetch the path

    try:
        # Get the file path first
        cursor.execute("SELECT path FROM gallery WHERE id = %s", (gallery_id,))
        row = cursor.fetchone()

        if not row:
            return JSONResponse(status_code=404, content={"error": "Gallery not found"})

        file_path = os.path.join(UPLOAD_FOLDER, row['path'])

        # Soft delete in DB
        cursor.execute("UPDATE gallery SET status = 0 WHERE id = %s", (gallery_id,))
        conn.commit()

        # Remove file from uploads folder if it exists
        if os.path.exists(file_path):
            os.remove(file_path)

        return {"message": "Gallery soft-deleted and file removed"}

    except Exception as e:
        conn.rollback()
        return JSONResponse(status_code=500, content={"error": str(e)})

    finally:
        conn.close()
