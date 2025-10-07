from fastapi import APIRouter, Depends, HTTPException, Request
from controllers import controllerWarranty
from utils.jwt_handler import get_current_user

router = APIRouter(prefix="/api/warranties", tags=["warranties"])
def require_permission(permission: str):
    def permission_checker(user=Depends(get_current_user)):
        if permission not in user["permissions"]:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return permission_checker


@router.get("/")
def get_all(user=Depends(require_permission("Read Warranties"))):
    return controllerWarranty.get_all_warranties()

@router.get("/{warranty_id}")
def get_one(warranty_id: int, user=Depends(require_permission("Read Warranties"))):
    return controllerWarranty.get_warranty_by_id(warranty_id)

@router.post("/create")
async def create(request: Request, user=Depends(require_permission("Create Warranties"))):
    data = await request.json()
    return controllerWarranty.create_warranty(data)

@router.put("/update/{warranty_id}")
async def update(warranty_id: int, request: Request, user=Depends(require_permission("Update Warranties"))):
    data = await request.json()
    return controllerWarranty.update_warranty(warranty_id, data)

@router.put("/delete/{warranty_id}")
def delete(warranty_id: int, user=Depends(require_permission("Delete Warranties"))):
    return controllerWarranty.delete_warranty(warranty_id)

@router.get("/all/public")
def get_all_public():
    return controllerWarranty.get_all_warranties_public()