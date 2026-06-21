from fastapi import APIRouter, HTTPException, Depends
from app.schemas.review import ReviewRequest, ReviewResponse
from app.services.openai_service import review_code
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/review", tags=["review"])

@router.post("", response_model=ReviewResponse)
def review_code_endpoint(payload: ReviewRequest, current_user: User = Depends(get_current_user)):
    try:
        return review_code(payload.code, payload.language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze code: {str(e)}")
