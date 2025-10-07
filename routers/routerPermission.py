from fastapi import APIRouter, Depends, HTTPException, Request
from controllers import controllerPermission
from utils.jwt_handler import get_current_user

router = APIRouter(prefix="/api/permissions", tags=["permissions"])

def require_permission(permission: str):
    def permission_checker(user=Depends(get_current_user)):
        if permission not in user["permissions"]:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return permission_checker

@router.get("/")
def get_all(user=Depends(require_permission("Read Permissions"))):
    return controllerPermission.get_all_permissions()

@router.get("/{permission_id}")
def get_one(permission_id: int, user=Depends(require_permission("Read Permissions"))):
    return controllerPermission.get_permission_by_id(permission_id)

@router.post("/create")
async def create(request: Request, user=Depends(require_permission("Create Permissions"))):
    data = await request.json()
    return controllerPermission.create_permission(data)

@router.put("/update/{permission_id}")
async def update(permission_id: int, request: Request, user=Depends(require_permission("Update Permissions"))):
    data = await request.json()
    return controllerPermission.update_permission(permission_id, data)

@router.put("/delete/{permission_id}")
def delete(permission_id: int, user=Depends(require_permission("Delete Permissions"))):
    return controllerPermission.delete_permission(permission_id)
