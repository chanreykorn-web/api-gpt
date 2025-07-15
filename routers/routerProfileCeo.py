from fastapi import APIRouter, Request
import controllers.controllerProfileCeo as controller

router = APIRouter(prefix="/ceo", tags=["Profile CEO"])

@router.get("/")
async def get_all():
    return controller.get_all_ceos()

@router.get("/{ceo_id}")
async def get_by_id(ceo_id: int):
    return controller.get_ceo_by_id(ceo_id)

@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controller.create_ceo(data)

@router.put("/update/{ceo_id}")
async def update(ceo_id: int, request: Request):
    data = await request.json()
    return controller.update_ceo(ceo_id, data)

@router.put("/delete/{ceo_id}")
async def delete(ceo_id: int):
    return controller.delete_ceo(ceo_id)
