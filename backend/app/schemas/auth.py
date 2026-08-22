from typing import List, Optional
from pydantic import BaseModel, EmailStr

class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    languages: List[str] = ["python"]
    self_declared_level: str = "intermediate"  # beginner, intermediate, advanced
    selected_topics: List[str] = []

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    languages: Optional[List[str]] = None
    self_declared_level: Optional[str] = None
    selected_topics: Optional[List[str]] = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    languages: List[str]
    self_declared_level: str
    selected_topics: List[str]
    knowledge_check_completed: bool

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
