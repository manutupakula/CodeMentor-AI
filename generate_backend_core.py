import os

BASE_DIR = r"C:\Users\Master_Manu\.gemini\antigravity\scratch\codementor-ai\backend"

def write_file(rel_path, content):
    full_path = os.path.join(BASE_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {rel_path}")

# app/core/config.py
write_file("app/core/config.py", """import os
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.7-flash"
    MONGODB_URI: str = ""
    MONGODB_DB_NAME: str = "codementor_db"
    JWT_SECRET: str = "super_secret_codementor_jwt_key_2026_change_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    JUDGE0_API_URL: str = ""
    JUDGE0_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str) and v.startswith("["):
            import json
            try:
                return json.loads(v)
            except Exception:
                return ["http://localhost:5173", "http://127.0.0.1:5173"]
        elif isinstance(v, list):
            return v
        return ["http://localhost:5173", "http://127.0.0.1:5173"]

    @property
    def is_gemini_configured(self) -> bool:
        return bool(self.GEMINI_API_KEY and self.GEMINI_API_KEY.strip())

settings = Settings()
""")

# app/core/security.py
write_file("app/core/security.py", """from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import bcrypt
import jwt
from app.core.config import settings

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": now})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except (jwt.PyJWTError, Exception):
        return None
""")

# app/db/mongodb.py
write_file("app/db/mongodb.py", """import logging
from typing import Optional, Any, Dict, List
import copy
import re

from app.core.config import settings

logger = logging.getLogger("codementor.db")

class AsyncInMemoryCollection:
    \"\"\"High-performance async in-memory document store matching PyMongo Async interface.\"\"\"
    def __init__(self, name: str):
        self.name = name
        self._documents: Dict[str, Dict[str, Any]] = {}

    def _matches(self, doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
        for k, v in query.items():
            if k == "$or":
                if not any(self._matches(doc, q) for q in v):
                    return False
                continue
            if k not in doc:
                return False
            doc_val = doc[k]
            if isinstance(v, dict):
                if "$in" in v:
                    if doc_val not in v["$in"]:
                        return False
                elif "$ne" in v:
                    if doc_val == v["$ne"]:
                        return False
                elif "$gt" in v:
                    if not (doc_val > v["$gt"]):
                        return False
                elif "$gte" in v:
                    if not (doc_val >= v["$gte"]):
                        return False
                elif "$lt" in v:
                    if not (doc_val < v["$lt"]):
                        return False
                elif "$lte" in v:
                    if not (doc_val <= v["$lte"]):
                        return False
                elif "$regex" in v:
                    pattern = v["$regex"]
                    options = v.get("$options", "")
                    flags = re.IGNORECASE if "i" in options else 0
                    if not re.search(pattern, str(doc_val), flags):
                        return False
            else:
                if doc_val != v:
                    return False
        return True

    async def insert_one(self, document: Dict[str, Any]):
        doc = copy.deepcopy(document)
        doc_id = str(doc.get("_id") or doc.get("id"))
        doc["_id"] = doc_id
        if "id" not in doc:
            doc["id"] = doc_id
        self._documents[doc_id] = doc
        class InsertResult:
            inserted_id = doc_id
        return InsertResult()

    async def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Fast path for _id or id
        if len(query) == 1 and ("_id" in query or "id" in query):
            target_id = str(query.get("_id") or query.get("id"))
            doc = self._documents.get(target_id)
            return copy.deepcopy(doc) if doc else None

        for doc in self._documents.values():
            if self._matches(doc, query):
                return copy.deepcopy(doc)
        return None

    def find(self, query: Optional[Dict[str, Any]] = None):
        query = query or {}
        matched = []
        for doc in self._documents.values():
            if not query or self._matches(doc, query):
                matched.append(copy.deepcopy(doc))
        
        class AsyncCursor:
            def __init__(self, docs):
                self._docs = docs
                self._idx = 0

            def sort(self, key_or_list, direction=1):
                if isinstance(key_or_list, list):
                    for key, d in reversed(key_or_list):
                        self._docs.sort(key=lambda x: str(x.get(key, "")), reverse=(d == -1))
                else:
                    self._docs.sort(key=lambda x: str(x.get(key_or_list, "")), reverse=(direction == -1))
                return self

            def limit(self, n: int):
                self._docs = self._docs[:n]
                return self

            def __aiter__(self):
                self._idx = 0
                return self

            async def __anext__(self):
                if self._idx < len(self._docs):
                    res = self._docs[self._idx]
                    self._idx += 1
                    return res
                raise StopAsyncIteration

            async def to_list(self, length: Optional[int] = None) -> List[Dict[str, Any]]:
                if length is not None:
                    return self._docs[:length]
                return self._docs

        return AsyncCursor(matched)

    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any], upsert: bool = False):
        doc = await self.find_one(query)
        if not doc:
            if upsert:
                new_doc = copy.deepcopy(query)
                if "$set" in update:
                    new_doc.update(update["$set"])
                doc_id = str(new_doc.get("_id") or new_doc.get("id", ""))
                new_doc["_id"] = doc_id
                self._documents[doc_id] = new_doc
                class UpsertResult:
                    matched_count = 0
                    modified_count = 1
                    upserted_id = doc_id
                return UpsertResult()
            class NoopResult:
                matched_count = 0
                modified_count = 0
            return NoopResult()

        doc_id = str(doc["_id"])
        target = self._documents[doc_id]
        if "$set" in update:
            for k, v in update["$set"].items():
                target[k] = copy.deepcopy(v)
        if "$inc" in update:
            for k, v in update["$inc"].items():
                target[k] = target.get(k, 0) + v
        if "$push" in update:
            for k, v in update["$push"].items():
                if k not in target or not isinstance(target[k], list):
                    target[k] = []
                target[k].append(copy.deepcopy(v))

        class UpdateResult:
            matched_count = 1
            modified_count = 1
        return UpdateResult()

    async def delete_one(self, query: Dict[str, Any]):
        doc = await self.find_one(query)
        if doc:
            doc_id = str(doc["_id"])
            if doc_id in self._documents:
                del self._documents[doc_id]
                class DeleteResult:
                    deleted_count = 1
                return DeleteResult()
        class DeleteResultZero:
            deleted_count = 0
        return DeleteResultZero()

    async def count_documents(self, query: Optional[Dict[str, Any]] = None) -> int:
        query = query or {}
        count = 0
        for doc in self._documents.values():
            if not query or self._matches(doc, query):
                count += 1
        return count

class AsyncInMemoryDatabase:
    def __init__(self, name: str):
        self.name = name
        self._collections: Dict[str, AsyncInMemoryCollection] = {}

    def __getitem__(self, name: str) -> AsyncInMemoryCollection:
        if name not in self._collections:
            self._collections[name] = AsyncInMemoryCollection(name)
        return self._collections[name]

    def get_collection(self, name: str) -> AsyncInMemoryCollection:
        return self[name]

class DatabaseManager:
    client: Any = None
    db: Any = None
    is_mock: bool = False

db_manager = DatabaseManager()

async def init_db():
    if settings.MONGODB_URI and settings.MONGODB_URI.strip():
        try:
            from pymongo import AsyncMongoClient
            db_manager.client = AsyncMongoClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=5000
            )
            db_manager.db = db_manager.client[settings.MONGODB_DB_NAME]
            # Ping to verify
            await db_manager.client.admin.command('ping')
            db_manager.is_mock = False
            logger.info("Connected to MongoDB Atlas successfully.")
            return
        except Exception as e:
            logger.warning(f"MongoDB connection failed: {e}. Falling back to Async InMemory Database.")
    
    # Fallback in-memory
    db_manager.db = AsyncInMemoryDatabase(settings.MONGODB_DB_NAME)
    db_manager.is_mock = True
    logger.info("Initialized Async InMemory Database for fast local/mock operation.")

async def close_db():
    if db_manager.client:
        try:
            await db_manager.client.close()
        except Exception:
            pass

def get_database():
    if db_manager.db is None:
        db_manager.db = AsyncInMemoryDatabase(settings.MONGODB_DB_NAME)
        db_manager.is_mock = True
    return db_manager.db

def get_collection(name: str):
    db = get_database()
    return db[name]
""")

print("Core modules created successfully.")
