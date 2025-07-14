from fastapi import APIRouter, Request, HTTPException
from controllers import controllerUsers

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_users():
    return controllerUsers.get_all_users()

@router.get("/{user_id}")
def get_user(user_id: int):
    user = controllerUsers.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/")
async def create_user(request: Request):
    data = await request.json()
    return controllerUsers.create_user(data)

@router.put("/{user_id}")
async def update_user(user_id: int, request: Request):
    data = await request.json()
    return controllerUsers.update_user(user_id, data)

@router.put("/delete/{user_id}")
def delete_user(user_id: int):
    return controllerUsers.delete_user(user_id)
