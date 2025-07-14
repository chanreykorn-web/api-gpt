from fastapi import APIRouter, Request, HTTPException
from controllers import controllerCategories

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/")
def get_all():
    return controllerCategories.get_all_categories()

@router.get("/{category_id}")
def get_by_id(category_id: int):
    category = controllerCategories.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controllerCategories.create_category(data)

@router.put("/update/{category_id}")
async def update(category_id: int, request: Request):
    data = await request.json()
    return controllerCategories.update_category(category_id, data)

@router.put("/delete/{category_id}")
def delete(category_id: int):
    return controllerCategories.delete_category(category_id)
