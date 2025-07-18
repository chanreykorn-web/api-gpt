from fastapi import APIRouter, Request
from controllers import controllerSpicification

router = APIRouter(prefix="/spicifications", tags=["spicifications"])

@router.get("/")
def get_all():
    return controllerSpicification.get_all_spicifications()

@router.get("/{spicification_id}")
def get_one(spicification_id: int):
    return controllerSpicification.get_spicification_by_id(spicification_id)

@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controllerSpicification.create_spicification(data)

@router.put("/update/{spicification_id}")
async def update(spicification_id: int, request: Request):
    data = await request.json()
    return controllerSpicification.update_spicification(spicification_id, data)

@router.put("/delete/{spicification_id}")
def delete(spicification_id: int):
    return controllerSpicification.delete_spicification(spicification_id)
