from fastapi import APIRouter, Request
import controllers.controllerIndustryDev as controller

router = APIRouter(prefix="/industry", tags=["Industry Development"])

@router.get("/")
async def get_all():
    return controller.get_all_industries()

@router.get("/{industry_id}")
async def get_by_id(industry_id: int):
    return controller.get_industry_by_id(industry_id)

@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controller.create_industry(data)

@router.put("/update/{industry_id}")
async def update(industry_id: int, request: Request):
    data = await request.json()
    return controller.update_industry(industry_id, data)

@router.put("/delete/{industry_id}")
async def delete(industry_id: int):
    return controller.delete_industry(industry_id)
