from fastapi import APIRouter, Request
import controllers.controllerNews as controllerNews

router = APIRouter(prefix="/news", tags=["News"])

@router.get("/")
async def get_all():
    return controllerNews.get_all_news()

@router.get("/{news_id}")
async def get_by_id(news_id: int):
    return controllerNews.get_news_by_id(news_id)

@router.post("/create")
async def create(request: Request):
    data = await request.json()
    return controllerNews.create_news(data)

@router.put("/update/{news_id}")
async def update(news_id: int, request: Request):
    data = await request.json()
    return controllerNews.update_news(news_id, data)

@router.put("/delete/{news_id}")
async def delete(news_id: int):
    return controllerNews.delete_news(news_id)
