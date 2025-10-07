from fastapi import APIRouter, UploadFile, File, Form, Request
from controllers import controllerGallery

router = APIRouter(prefix="/api/gallery", tags=["Gallery"])

@router.post("/create")
async def create_gallery(
    file: UploadFile = File(...),
    user_id: int = Form(...),
    image_id: int = Form(None)
):
    return controllerGallery.create_gallery(file, user_id, image_id)

@router.get("/")
async def get_all():
    return controllerGallery.get_all_gallery()

@router.get("/{gallery_id}")
async def get_by_id(gallery_id: int):
    return controllerGallery.get_gallery_by_id(gallery_id)

@router.put("/{gallery_id}")
async def update_gallery(gallery_id: int, request: Request):
    data = await request.json()
    return controllerGallery.update_gallery(gallery_id, data)

@router.delete("/{gallery_id}")
async def delete_gallery(gallery_id: int):
    return controllerGallery.delete_gallery(gallery_id)
