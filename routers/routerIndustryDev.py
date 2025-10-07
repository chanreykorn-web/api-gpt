from fastapi import APIRouter, Depends, HTTPException, Request
import controllers.controllerIndustryDev as controller
from utils.jwt_handler import get_current_user

router = APIRouter(prefix="/api/industry", tags=["Industry Development"])

def require_permission(permission: str):
    def permission_checker(user=Depends(get_current_user)):
        if permission not in user["permissions"]:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return permission_checker

@router.get("/")
async def get_all(user=Depends(require_permission("Read Industries"))):
    return controller.get_all_industries()

@router.get("/{industry_id}")
async def get_by_id(industry_id: int, user=Depends(require_permission("Read Industries"))):
    return controller.get_industry_by_id(industry_id)

@router.post("/create")
async def create(request: Request, user=Depends(require_permission("Create Industries"))):
    data = await request.json()
    return controller.create_industry(data)

@router.put("/update/{industry_id}")
async def update(industry_id: int, request: Request, user=Depends(require_permission("Update Industries"))):
    data = await request.json()
    return controller.update_industry(industry_id, data)

@router.put("/delete/{industry_id}")
async def delete(industry_id: int, user=Depends(require_permission("Delete Industries"))):
    return controller.delete_industry(industry_id)

@router.get("/all/public")
async def get_all_public():
    return controller.get_all_industries_public()