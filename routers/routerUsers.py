from fastapi import APIRouter, Depends, HTTPException, Request
import controllers.controllerUsers as user_ctrl
from utils.jwt_handler import get_current_user

router = APIRouter(prefix="/api/users", tags=["Users"])

def require_permission(permission: str):
    def permission_checker(user=Depends(get_current_user)):
        if permission not in user["permissions"]:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return permission_checker

@router.get("/")
def get_all(user=Depends(require_permission("Read Users"))):
    return user_ctrl.get_all_users()

@router.get("/{user_id}")
def get_one(user_id: int, user=Depends(require_permission("Read Users"))):
    return user_ctrl.get_user_by_id(user_id)

@router.post("/create")
async def create(request: Request, user=Depends(require_permission("Create Users"))):
    data = await request.json()  # await here!
    return user_ctrl.create_user(data)

@router.put("/update/{user_id}")
async def update(user_id: int, request: Request, user=Depends(require_permission("Update Users"))):
    data = await request.json()   # <-- await here
    return user_ctrl.update_user(user_id, data)

@router.put("/delete/{user_id}")
def delete(user_id: int, user=Depends(require_permission("Delete Users"))):
    return user_ctrl.delete_user(user_id)
