from fastapi import APIRouter, Request
from controllers import controllerGallery

router = APIRouter(prefix="/gallery", tags=["Gallery"])

@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controllerGallery.create_gallery(data)

@router.get("/")
async def get_all():
    return controllerGallery.get_all_gallery()

@router.get("/{gallery_id}")
async def get_by_id(gallery_id: int):
    return controllerGallery.get_gallery_by_id(gallery_id)

@router.put("/update/{gallery_id}")
async def update(gallery_id: int, request: Request):
    data = await request.json()
    return controllerGallery.update_gallery(gallery_id, data)

@router.put("/delete/{gallery_id}")
async def delete(gallery_id: int):
    return controllerGallery.delete_gallery(gallery_id)
