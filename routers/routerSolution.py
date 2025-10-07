from fastapi import APIRouter, Depends, HTTPException, Request
from controllers import controllerSolution
from utils.jwt_handler import get_current_user

router = APIRouter(prefix="/api/solutions", tags=["solutions"])

def require_permission(permission: str):
    def permission_checker(user=Depends(get_current_user)):
        if permission not in user["permissions"]:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return permission_checker

@router.get("/")
def get_all(user=Depends(require_permission("Read Solutions"))):
    return controllerSolution.get_all_solutions()

@router.get("/{solution_id}")
def get_one(solution_id: int, user=Depends(require_permission("Read Solutions"))):
    return controllerSolution.get_solution_by_id(solution_id)

@router.post("/create")
async def create(request: Request, user=Depends(require_permission("Create Solutions"))):
    data = await request.json()
    return controllerSolution.create_solution(data)

@router.put("/update/{solution_id}")
async def update(solution_id: int, request: Request, user=Depends(require_permission("Update Solutions"))):
    data = await request.json()
    return controllerSolution.update_solution(solution_id, data)

@router.put("/delete/{solution_id}")
def delete(solution_id: int, user=Depends(require_permission("Delete Solutions"))):
    return controllerSolution.delete_solution(solution_id)

@router.get("/all/public")
def get_all_public():
    return controllerSolution.get_all_solutions_public()

@router.get("/all/public/{solution_id}")
def get_one(solution_id: int):
    return controllerSolution.get_solution_public_by_id(solution_id)