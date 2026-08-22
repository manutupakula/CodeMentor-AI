import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import uuid

from app.db.mongodb import get_collection
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.services.learner_service import learner_service
from app.utils.errors import InvalidCredentialsError, EntityNotFoundError

logger = logging.getLogger("codementor.auth_service")

class AuthService:
    @staticmethod
    async def register_user(
        name: str,
        email: str,
        password: str,
        languages: list = None,
        self_declared_level: str = "intermediate",
        selected_topics: list = None
    ) -> Dict[str, Any]:
        users_col = get_collection("users")
        existing = await users_col.find_one({"email": email.lower().strip()})
        if existing:
            raise InvalidCredentialsError("User with this email already exists.")

        user_id = str(uuid.uuid4())
        user_doc = {
            "_id": user_id,
            "id": user_id,
            "name": name.strip(),
            "email": email.lower().strip(),
            "password_hash": hash_password(password),
            "languages": languages or ["python"],
            "self_declared_level": self_declared_level.lower(),
            "selected_topics": selected_topics or [],
            "knowledge_check_completed": False,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }

        await users_col.insert_one(user_doc)
        
        # Initialize learner profile
        await learner_service.get_or_create_profile(user_id, self_declared_level)

        access_token = create_access_token({"sub": user_id, "email": user_doc["email"]})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user_id,
                "name": user_doc["name"],
                "email": user_doc["email"],
                "languages": user_doc["languages"],
                "self_declared_level": user_doc["self_declared_level"],
                "selected_topics": user_doc["selected_topics"],
                "knowledge_check_completed": False
            }
        }

    @staticmethod
    async def login_user(email: str, password: str) -> Dict[str, Any]:
        users_col = get_collection("users")
        user = await users_col.find_one({"email": email.lower().strip()})
        if not user or not verify_password(password, user["password_hash"]):
            raise InvalidCredentialsError("Invalid email or password.")

        user_id = str(user.get("_id") or user.get("id"))
        access_token = create_access_token({"sub": user_id, "email": user["email"]})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user_id,
                "name": user["name"],
                "email": user["email"],
                "languages": user.get("languages", ["python"]),
                "self_declared_level": user.get("self_declared_level", "intermediate"),
                "selected_topics": user.get("selected_topics", []),
                "knowledge_check_completed": user.get("knowledge_check_completed", False)
            }
        }

    @staticmethod
    async def get_current_user(token: str) -> Dict[str, Any]:
        payload = decode_access_token(token)
        if not payload or "sub" not in payload:
            raise InvalidCredentialsError("Invalid or expired authentication token.")

        user_id = payload["sub"]
        users_col = get_collection("users")
        user = await users_col.find_one({"_id": user_id}) or await users_col.find_one({"id": user_id})
        if not user:
            raise EntityNotFoundError("User account not found.")

        return user

auth_service = AuthService()
