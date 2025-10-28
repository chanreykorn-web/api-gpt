from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


# Router imports
from routers import (
    routerUsers,
    routerAuth,
    routerRole,
    routerCategories,
    routerProduct,
    routerBanner,
    routerGallery,
    routerMission,
    routerNews,
    routerWelcome,
    routerProfileCeo,
    routerIndustryDev,
    routerContact,
    routerFormContact,
    routerChooseUs,
    routerSolution,
    routerWarranty,
    routerPermission,
    routerRolePermission,
    routerSpicification,
)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    'http://172.28.96.1:5173',
    "http://10.90.46.216:5173",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://172.28.96.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],          # Allow all HTTP methods
    allow_headers=["*"],          # Allow all headers
)

# Include routers
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
app.include_router(routerChooseUs.router)
app.include_router(routerSolution.router)
app.include_router(routerWarranty.router)
app.include_router(routerPermission.router)
app.include_router(routerRolePermission.router)
app.include_router(routerSpicification.router)
app.include_router(routerGallery.router)
app.mount("/api/uploads", StaticFiles(directory="uploads"), name="uploads")


# Include your gallery API router

app.include_router(routerGallery.router, prefix="/api/gallery", tags=["Gallery"])



@app.get("/")
def root():
    return {"message": "API is running securely 🎉"}
