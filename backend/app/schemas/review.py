from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class ReviewRequest(BaseModel):
    code: str = Field(..., description="The source code or unified diff to be reviewed")
    language: Optional[str] = Field(None, description="Programming language of the code (optional)")

class ReviewComment(BaseModel):
    line_number: int = Field(..., description="The 1-based line number in the submitted code/diff where this issue exists")
    severity: Literal["critical", "warning", "info"] = Field(..., description="The level of importance of the review comment")
    message: str = Field(..., description="The explanation of the bug, issue, or improvement area")
    suggestion: str = Field(..., description="Code suggestion or recommended fix")

class ReviewResponse(BaseModel):
    comments: List[ReviewComment] = Field(default_factory=list, description="List of generated review comments")
