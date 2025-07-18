from fastapi import APIRouter, Request
import controllers.controllerUsers as user_ctrl

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_all():
    return user_ctrl.get_all_users()

@router.get("/{user_id}")
def get_one(user_id: int):
    return user_ctrl.get_user_by_id(user_id)

@router.post("/create")
async def create(request: Request):
    data = await request.json()  # await here!
    return user_ctrl.create_user(data)

@router.put("/{user_id}")
def update(user_id: int, request: Request):
    data = request.json()
    return user_ctrl.update_user(user_id, data)

@router.delete("/{user_id}")
def delete(user_id: int):
    return user_ctrl.delete_user(user_id)
