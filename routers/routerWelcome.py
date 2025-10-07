from fastapi import APIRouter, Depends, HTTPException, Request
from controllers import controllerWelcome
from utils.jwt_handler import get_current_user

router = APIRouter(prefix="/api/welcome", tags=["Welcome"])

def require_permission(permission: str):
    def permission_checker(user=Depends(get_current_user)):
        if permission not in user["permissions"]:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return permission_checker

@router.get("/")
async def get_all(user=Depends(require_permission("Read Welcome"))):
    return controllerWelcome.get_all_welcome()

@router.get("/{welcome_id}")
async def get_by_id(welcome_id: int, user=Depends(require_permission("Read Welcome"))):
    return controllerWelcome.get_welcome_by_id(welcome_id)

@router.post("/create")
async def create(request: Request, user=Depends(require_permission("Create Welcome"))):
    data = await request.json()
    return controllerWelcome.create_welcome(data)

@router.put("/update/{welcome_id}")
async def update(welcome_id: int, request: Request, user=Depends(require_permission("Update Welcome"))):
    data = await request.json()
    return controllerWelcome.update_welcome(welcome_id, data)

@router.put("/delete/{welcome_id}")
async def delete(welcome_id: int, user=Depends(require_permission("Delete Welcome"))):
    return controllerWelcome.delete_welcome(welcome_id)

@router.get("/all/public")
async def get_all_public():
    return controllerWelcome.get_all_welcome_public()
