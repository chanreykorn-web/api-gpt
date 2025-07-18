from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    "http://localhost:5173",  # Vite dev server
    # Add other allowed origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Or ["*"] to allow all during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/")
def root():
    return {"message": "API is running securely 🎉"}
