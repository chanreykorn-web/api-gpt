from fastapi import APIRouter, Depends, Request, HTTPException
from controllers import controllerRole
from utils.jwt_handler import get_current_user

router = APIRouter(prefix="/api/roles", tags=["Roles"])

def require_permission(permission: str):
    def permission_checker(user=Depends(get_current_user)):
        if permission not in user["permissions"]:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return permission_checker

@router.get("/")
def get_all(user=Depends(require_permission("Read Roles"))):
    return controllerRole.get_all_roles()

@router.get("/{role_id}")
def get_one(role_id: int, user=Depends(require_permission("Read Roles"))):
    role = controllerRole.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.post("/create")
async def create(request: Request, user=Depends(require_permission("Create Roles"))):
    data = await request.json()
    return controllerRole.create_role(data)

@router.put("/update/{role_id}")
async def update(role_id: int, request: Request, user=Depends(require_permission("Update Roles"))):
    data = await request.json()
    return controllerRole.update_role(role_id, data)

@router.put("/delete/{role_id}")
def delete(role_id: int, user=Depends(require_permission("Delete Roles"))):
    return controllerRole.delete_role(role_id)


@router.get("/role/me")
def get_me(payload: dict = Depends(get_current_user)):
    return {
        "email": payload["sub"],
        "role": payload["role"],
        "user_id": payload["user_id"],
        "permissions": payload["permissions"]
    }