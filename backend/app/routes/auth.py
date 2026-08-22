from fastapi import APIRouter, Depends, Header, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse, UserResponse
from app.services.auth_service import auth_service
from app.utils.errors import InvalidCredentialsError

router = APIRouter(prefix="/api/auth", tags=["Auth"])
security = HTTPBearer(auto_error=False)

async def get_current_user_dep(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    if not credentials or not credentials.credentials:
        raise InvalidCredentialsError("Missing authentication token")
    return await auth_service.get_current_user(credentials.credentials)

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(req: UserRegisterRequest):
    return await auth_service.register_user(
        name=req.name,
        email=req.email,
        password=req.password,
        languages=req.languages,
        self_declared_level=req.self_declared_level,
        selected_topics=req.selected_topics
    )

@router.post("/login", response_model=TokenResponse)
async def login(req: UserLoginRequest):
    return await auth_service.login_user(
        email=req.email,
        password=req.password
    )

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user_dep)):
    return {
        "id": str(current_user.get("_id") or current_user.get("id")),
        "name": current_user["name"],
        "email": current_user["email"],
        "languages": current_user.get("languages", ["python"]),
        "self_declared_level": current_user.get("self_declared_level", "intermediate"),
        "selected_topics": current_user.get("selected_topics", []),
        "knowledge_check_completed": current_user.get("knowledge_check_completed", False)
    }
