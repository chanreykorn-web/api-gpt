from fastapi import APIRouter, Request, HTTPException
from controllers import controllerRole

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/")
def get_all():
    return controllerRole.get_all_roles()

@router.get("/{role_id}")
def get_one(role_id: int):
    role = controllerRole.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controllerRole.create_role(data)

@router.put("/update/{role_id}")
async def update(role_id: int, request: Request):
    data = await request.json()
    return controllerRole.update_role(role_id, data)

@router.put("/delete/{role_id}")
def delete(role_id: int):
    return controllerRole.delete_role(role_id)