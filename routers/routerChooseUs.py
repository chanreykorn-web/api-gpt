from fastapi import APIRouter, Request, Depends, HTTPException, status
import controllers.controllerChooseUs as controller
from utils.jwt_handler import get_current_user

router = APIRouter(prefix="/api/choose-us", tags=["Choose Us"])

def require_permission(permission: str):
    def permission_checker(user=Depends(get_current_user)):
        if permission not in user["permissions"]:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return permission_checker

@router.get("/")
async def get_all(user=Depends(require_permission("Read choose us"))):
    return controller.get_all_choose_us()

@router.get("/{choose_id}")
async def get_by_id(choose_id: int, user=Depends(require_permission("Read choose us"))):
    return controller.get_choose_us_by_id(choose_id)

@router.post("/create")
async def create(request: Request, user=Depends(require_permission("Create choose us"))):
    data = await request.json()
    return controller.create_choose_us(data)

@router.put("/update/{choose_id}")
async def update(choose_id: int, request: Request, user=Depends(require_permission("Update choose us"))):
    data = await request.json()
    return controller.update_choose_us(choose_id, data)

@router.put("/delete/{choose_id}")
async def delete(choose_id: int, user=Depends(require_permission("Delete choose us"))):
    return controller.delete_choose_us(choose_id)

@router.get("/all/public")
async def get_all_public():
    return controller.get_all_choose_us_public()

# @router.get("/all/public/{choose_id}")
# async def get_all_public(choose_id: int,):
#     return controller.get_by_id_choose_us_public(choose_id)


@router.get("/all/public/{choose_id}")
async def get_by_id_public(choose_id: int):
    return controller.get_choose_us_by_id_public(choose_id)

@router.put("/our/process/all/public/{choose_id}")
async def update(choose_id: int, request: Request, user=Depends(require_permission("Update choose us"))):
    data = await request.json()
    return controller.get_process_public(choose_id, data)