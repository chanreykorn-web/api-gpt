from fastapi import APIRouter, Request, Depends
import controllers.controllerBanner as controllerBanner
from auth_dependencies import require_permission
from fastapi import APIRouter, Depends, HTTPException, status
from utils.jwt_handler import get_current_user 

router = APIRouter(prefix="/banners")


from fastapi import Depends, HTTPException, status

def require_permission(permission: str):
    def permission_checker(user=Depends(get_current_user)):
        if permission not in user["permissions"]:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return permission_checker

@router.get("/")
async def get_all(user=Depends(require_permission("can_view"))):
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

@router.delete("/delete/{banner_id}")
async def delete(banner_id: int):  # ✅ check permission only here
    return controllerBanner.delete_banner(banner_id)
