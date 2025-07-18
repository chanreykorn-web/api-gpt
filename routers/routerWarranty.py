from fastapi import APIRouter, Request
from controllers import controllerWarranty

router = APIRouter(prefix="/warranties", tags=["warranties"])

@router.get("/")
def get_all():
    return controllerWarranty.get_all_warranties()

@router.get("/{warranty_id}")
def get_one(warranty_id: int):
    return controllerWarranty.get_warranty_by_id(warranty_id)

@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controllerWarranty.create_warranty(data)

@router.put("/update/{warranty_id}")
async def update(warranty_id: int, request: Request):
    data = await request.json()
    return controllerWarranty.update_warranty(warranty_id, data)

@router.put("/delete/{warranty_id}")
def delete(warranty_id: int):
    return controllerWarranty.delete_warranty(warranty_id)
