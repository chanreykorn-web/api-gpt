from fastapi import APIRouter, Depends, HTTPException, Request
from controllers import controllerSpicification
from utils.jwt_handler import get_current_user

router = APIRouter(prefix="/api/spicifications", tags=["spicifications"])

def require_permission(permission: str):
    def permission_checker(user=Depends(get_current_user)):
        if permission not in user["permissions"]:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return permission_checker

@router.get("/")
def get_all(user=Depends(require_permission("Read Spicifications"))):
    return controllerSpicification.get_all_spicifications()

@router.get("/{spicification_id}")
def get_one(spicification_id: int, user=Depends(require_permission("Read Spicifications"))):
    return controllerSpicification.get_spicification_by_id(spicification_id)

@router.post("/create")
async def create(request: Request, user=Depends(require_permission("Create Spicifications"))):
    data = await request.json()
    return controllerSpicification.create_spicification(data)

@router.put("/update/{spicification_id}")
async def update(spicification_id: int, request: Request, user=Depends(require_permission("Update Spicifications"))):
    data = await request.json()
    return controllerSpicification.update_spicification(spicification_id, data)

@router.put("/delete/{spicification_id}")
def delete(spicification_id: int, user=Depends(require_permission("Delete Spicifications"))):
    return controllerSpicification.delete_spicification(spicification_id)
