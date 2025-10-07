from fastapi import APIRouter, Request, Depends
import controllers.controllerBanner as controllerBanner
from auth_dependencies import require_permission
from fastapi import APIRouter, Depends, HTTPException, status
from utils.jwt_handler import get_current_user 

router = APIRouter(prefix="/api/banners")


from fastapi import Depends, HTTPException, status

def require_permission(permission: str):
    def permission_checker(user=Depends(get_current_user)):
        if permission not in user["permissions"]:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return permission_checker

@router.get("/")
async def get_all(user=Depends(require_permission("Read banners"))):
    return controllerBanner.get_all_banners()

@router.get("/{banner_id}")
async def get_by_id(banner_id: int, user=Depends(require_permission("Read banners"))):
    return controllerBanner.get_banner_by_id(banner_id)

@router.post("/create")
async def create(request: Request, user=Depends(require_permission("Create banners"))):
    data = await request.json()
    return controllerBanner.create_banner(data)

@router.put("/update/{banner_id}")
async def update(banner_id: int, request: Request, user=Depends(require_permission("Update banners"))):
    data = await request.json()
    return controllerBanner.update_banner(banner_id, data)

@router.delete("/delete/{banner_id}")
async def delete(banner_id: int, user=Depends(require_permission("Delete banners"))):
    return controllerBanner.delete_banner(banner_id)


@router.get("/all/public")
async def public_banners():
    return controllerBanner.get_all_banners_public()

@router.get("/all/public/{banner_type}")
async def public_banners_type(banner_type: int):
    return controllerBanner.get_banner_by_type(banner_type)


@router.put("/set-type/{banner_id}")
async def set_type(banner_id: int, request: Request, user=Depends(require_permission("Update banners"))):
    data = await request.json()
    banner_type = data.get("type")
    if not banner_type:
        raise HTTPException(status_code=400, detail="type is required")
    return controllerBanner.set_banner_type(banner_id, banner_type)