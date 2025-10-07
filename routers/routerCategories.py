from fastapi import APIRouter, Depends, Request, HTTPException
from controllers import controllerCategories
from auth_dependencies import require_permission
from utils.jwt_handler import get_current_user


router = APIRouter(prefix="/api/categories", tags=["Categories"])

def require_permission(permission: str):
    def permission_checker(user=Depends(get_current_user)):
        if permission not in user["permissions"]:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return permission_checker

@router.get("/")
def get_all(user=Depends(require_permission("Read Categories"))):
    return controllerCategories.get_all_categories()

@router.get("/{category_id}")
def get_by_id(category_id: int, user=Depends(require_permission("Read Categories"))):
    category = controllerCategories.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/create")
async def create(request: Request, user=Depends(require_permission("Create Categories"))):
    data = await request.json()
    return controllerCategories.create_category(data)

@router.put("/update/{category_id}")
async def update(category_id: int, request: Request, user=Depends(require_permission("Update Categories"))):
    data = await request.json()
    return controllerCategories.update_category(category_id, data)

@router.put("/delete/{category_id}")
def delete(category_id: int, user=Depends(require_permission("Delete Categories"))):
    return controllerCategories.delete_category(category_id)


@router.get("/all/public")
def get_all():
    return controllerCategories.get_all_categories_public()