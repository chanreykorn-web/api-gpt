from fastapi import APIRouter, Request
from controllers import controllerProduct

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/")
def get_all():
    return controllerProduct.get_all_products()

@router.get("/{product_id}")
def get_one(product_id: int):
    return controllerProduct.get_product_by_id(product_id)

@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controllerProduct.create_product(data)

@router.put("/update/{product_id}")
async def update(product_id: int, request: Request):
    data = await request.json()
    return controllerProduct.update_product(product_id, data)

@router.put("/delete/{product_id}")
def delete(product_id: int):
    return controllerProduct.delete_product(product_id)
