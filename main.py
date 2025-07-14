from fastapi import FastAPI
from routers import routerUsers
from routers import routerAuth
from routers import routerRole
from routers import routerCategories

app = FastAPI()

app.include_router(routerUsers.router)
app.include_router(routerAuth.router)
app.include_router(routerRole.router)
app.include_router(routerCategories.router)


@app.get("/")
def root():
    return {"message": "API is running"}
