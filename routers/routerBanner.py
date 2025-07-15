from fastapi import APIRouter, Request
import controllers.controllerBanner as controllerBanner

router = APIRouter(prefix="/banners", tags=["Banners"])

@router.get("/")
async def get_all():
    return controllerBanner.get_all_banners()

@router.get("/{banner_id}")
async def get_by_id(banner_id: int):
    return controllerBanner.get_banner_by_id(banner_id)

@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controllerBanner.create_banner(data)

@router.put("/update/{banner_id}")
async def update(banner_id: int, request: Request):
    data = await request.json()
    return controllerBanner.update_banner(banner_id, data)

@router.put("/delete/{banner_id}")
async def delete(banner_id: int):
    return controllerBanner.delete_banner(banner_id)
