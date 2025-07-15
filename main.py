from fastapi import FastAPI
from routers import routerUsers
from routers import routerAuth
from routers import routerRole
from routers import routerCategories
from routers import routerProduct
from routers import routerBanner
from routers import routerGallery
from routers import routerMission
from routers import routerNews
from routers import routerWelcome
from routers import routerProfileCeo
from routers import routerIndustryDev
from routers import routerContact
from routers import routerFormContact

app = FastAPI()

app.include_router(routerUsers.router)
app.include_router(routerAuth.router)
app.include_router(routerRole.router)
app.include_router(routerCategories.router)
app.include_router(routerProduct.router)
app.include_router(routerBanner.router)
app.include_router(routerGallery.router)
app.include_router(routerMission.router)
app.include_router(routerNews.router)
app.include_router(routerWelcome.router)
app.include_router(routerProfileCeo.router)
app.include_router(routerIndustryDev.router)
app.include_router(routerContact.router)
app.include_router(routerFormContact.router)


@app.get("/")
def root():
    return {"message": "API is running"}

# print('http://127.0.0.1:8000')
