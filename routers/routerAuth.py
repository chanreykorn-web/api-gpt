from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.jwt_handler import create_access_token
from controllers.controllerUsers import get_user_from_db
from security import pwd_context
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/api/auth")

class LoginRequest(BaseModel):
    username: str
    password: str

from controllers.controllerUsers import get_user_from_db, get_user_permissions

@router.post("/login")
def login(request: LoginRequest):
    user = get_user_from_db(request.username)
    if not user or not pwd_context.verify(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    permissions = get_user_permissions(user["id"])

    access_token = create_access_token({
        "sub": user["username"],
        "role": user["role"],
        "user_id": user["id"],
        "permissions": permissions
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user["role"],
        "user_id": user["id"],
        "permissions": permissions
    }

