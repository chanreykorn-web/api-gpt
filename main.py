from fastapi import FastAPI
from routers import routerUsers
from routers import routerAuth
from routers import routerRole

app = FastAPI()

app.include_router(routerUsers.router)
app.include_router(routerAuth.router)
app.include_router(routerRole.router)


@app.get("/")
def root():
    return {"message": "API is running"}
