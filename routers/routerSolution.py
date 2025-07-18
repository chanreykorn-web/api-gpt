from fastapi import APIRouter, Request
from controllers import controllerSolution

router = APIRouter(prefix="/solutions", tags=["solutions"])

@router.get("/")
def get_all():
    return controllerSolution.get_all_solutions()

@router.get("/{solution_id}")
def get_one(solution_id: int):
    return controllerSolution.get_solution_by_id(solution_id)

@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controllerSolution.create_solution(data)

@router.put("/update/{solution_id}")
async def update(solution_id: int, request: Request):
    data = await request.json()
    return controllerSolution.update_solution(solution_id, data)

@router.put("/delete/{solution_id}")
def delete(solution_id: int):
    return controllerSolution.delete_solution(solution_id)
