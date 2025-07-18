from fastapi import APIRouter, Request
from controllers import controllerPermission

router = APIRouter(prefix="/permissions", tags=["permissions"])

@router.get("/")
def get_all():
    return controllerPermission.get_all_permissions()

@router.get("/{permission_id}")
def get_one(permission_id: int):
    return controllerPermission.get_permission_by_id(permission_id)

@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controllerPermission.create_permission(data)

@router.put("/update/{permission_id}")
async def update(permission_id: int, request: Request):
    data = await request.json()
    return controllerPermission.update_permission(permission_id, data)

@router.put("/delete/{permission_id}")
def delete(permission_id: int):
    return controllerPermission.delete_permission(permission_id)
