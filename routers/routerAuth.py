from fastapi import APIRouter, Request, HTTPException, Header, Depends
from controllers import controllerAuth
from auth import create_access_token, decode_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    user = controllerAuth.login_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["username"], "id": user["id"]})
    return {"access_token": token}

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

@router.get("/me")
def get_profile(user: dict = Depends(get_current_user)):
    return {"user": user}
