from fastapi import APIRouter, Request
from controllers import controllerWelcome

router = APIRouter(prefix="/welcome", tags=["Welcome"])

@router.get("/")
async def get_all():
    return controllerWelcome.get_all_welcome()

@router.get("/{welcome_id}")
async def get_by_id(welcome_id: int):
    return controllerWelcome.get_welcome_by_id(welcome_id)

@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controllerWelcome.create_welcome(data)

@router.put("/update/{welcome_id}")
async def update(welcome_id: int, request: Request):
    data = await request.json()
    return controllerWelcome.update_welcome(welcome_id, data)

@router.put("/delete/{welcome_id}")
async def delete(welcome_id: int):
    return controllerWelcome.delete_welcome(welcome_id)
