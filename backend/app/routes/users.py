from fastapi import APIRouter, Depends
from datetime import datetime, timezone
from app.schemas.auth import UserResponse, UserProfileUpdateRequest
from app.routes.auth import get_current_user_dep
from app.db.mongodb import get_collection

router = APIRouter(prefix="/api/profile", tags=["User Profile"])

@router.get("", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_user_dep)):
    return {
        "id": str(current_user.get("_id") or current_user.get("id")),
        "name": current_user["name"],
        "email": current_user["email"],
        "languages": current_user.get("languages", ["python"]),
        "self_declared_level": current_user.get("self_declared_level", "intermediate"),
        "selected_topics": current_user.get("selected_topics", []),
        "knowledge_check_completed": current_user.get("knowledge_check_completed", False)
    }

@router.put("", response_model=UserResponse)
async def update_profile(
    req: UserProfileUpdateRequest,
    current_user: dict = Depends(get_current_user_dep)
):
    user_id = str(current_user.get("_id") or current_user.get("id"))
    users_col = get_collection("users")
    
    update_fields = {"updated_at": datetime.now(timezone.utc)}
    if req.name is not None:
        update_fields["name"] = req.name
    if req.languages is not None:
        update_fields["languages"] = req.languages
    if req.self_declared_level is not None:
        update_fields["self_declared_level"] = req.self_declared_level.lower()
    if req.selected_topics is not None:
        update_fields["selected_topics"] = req.selected_topics

    await users_col.update_one({"_id": user_id}, {"$set": update_fields})
    updated_user = await users_col.find_one({"_id": user_id})

    return {
        "id": user_id,
        "name": updated_user["name"],
        "email": updated_user["email"],
        "languages": updated_user.get("languages", ["python"]),
        "self_declared_level": updated_user.get("self_declared_level", "intermediate"),
        "selected_topics": updated_user.get("selected_topics", []),
        "knowledge_check_completed": updated_user.get("knowledge_check_completed", False)
    }
