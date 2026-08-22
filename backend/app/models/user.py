from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class UserModel(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: EmailStr
    password_hash: str
    languages: List[str] = ["python"]
    self_declared_level: str = "intermediate"  # beginner, intermediate, advanced
    selected_topics: List[str] = []
    knowledge_check_completed: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }
