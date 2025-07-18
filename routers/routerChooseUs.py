from fastapi import APIRouter, Request
import controllers.controllerChooseUs as controller

router = APIRouter(prefix="/choose-us", tags=["Choose Us"])

@router.get("/")
async def get_all():
    return controller.get_all_choose_us()

@router.get("/{choose_id}")
async def get_by_id(choose_id: int):
    return controller.get_choose_us_by_id(choose_id)

@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controller.create_choose_us(data)

@router.put("/update/{choose_id}")
async def update(choose_id: int, request: Request):
    data = await request.json()
    return controller.update_choose_us(choose_id, data)

@router.put("/delete/{choose_id}")
async def put(choose_id: int):
    return controller.delete_choose_us(choose_id)
