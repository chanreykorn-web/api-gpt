from fastapi import APIRouter, Request
import controllers.controllerContact as controller

router = APIRouter(prefix="/contacts", tags=["Contact Us"])

@router.get("/")
async def get_all():
    return controller.get_all_contacts()

@router.get("/{contact_id}")
async def get_by_id(contact_id: int):
    return controller.get_contact_by_id(contact_id)

@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controller.create_contact(data)

@router.put("/update/{contact_id}")
async def update(contact_id: int, request: Request):
    data = await request.json()
    return controller.update_contact(contact_id, data)

@router.delete("/delete/{contact_id}")
async def delete(contact_id: int):
    return controller.delete_contact(contact_id)
