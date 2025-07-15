from fastapi import APIRouter, Request
from controllers import controllerMission

router = APIRouter(prefix="/missions", tags=["Mission"])


@router.get("/")
async def get_all():
    return controllerMission.get_all_missions()


@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controllerMission.create_mission(data)

@router.put("/update/{mission_id}")
async def update(mission_id: int, request: Request):
    data = await request.json()
    return controllerMission.update_mission(mission_id, data)

@router.put("/delete/{mission_id}")
async def delete(mission_id: int):
    return controllerMission.delete_mission(mission_id)
