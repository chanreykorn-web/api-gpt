from fastapi import APIRouter, Request
from controllers import controllerRolePermission

router = APIRouter(prefix="/role-permissions", tags=["role_permissions"])

@router.get("/")
def get_all():
    return controllerRolePermission.get_all_role_permissions()

@router.get("/{role_permission_id}")
def get_one(role_permission_id: int):
    return controllerRolePermission.get_role_permission_by_id(role_permission_id)

@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controllerRolePermission.create_role_permission(data)

@router.put("/update/{role_permission_id}")
async def update(role_permission_id: int, request: Request):
    data = await request.json()
    return controllerRolePermission.update_role_permission(role_permission_id, data)

@router.put("/delete/{role_permission_id}")
def delete(role_permission_id: int):
    return controllerRolePermission.delete_role_permission(role_permission_id)
