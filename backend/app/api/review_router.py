from fastapi import APIRouter, HTTPException
from app.schemas.review import ReviewRequest, ReviewResponse, ReviewComment

router = APIRouter(prefix="/review", tags=["review"])

@router.post("", response_model=ReviewResponse)
def review_code_endpoint(payload: ReviewRequest):
    # Initial basic endpoint returning empty list or simple mock
    mock_comments = [
        ReviewComment(
            line_number=1,
            severity="info",
            message="Endpoint received code review request successfully.",
            suggestion="No changes needed."
        )
    ]
    return ReviewResponse(comments=mock_comments)
