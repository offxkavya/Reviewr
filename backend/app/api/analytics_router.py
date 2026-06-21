from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/metrics")
def get_metrics():
    # In a real scenario, these would be aggregated via SQLAlchemy queries
    # e.g., grouping reviews by user, severity, status over time
    return {
        "velocity": {
            "avg_review_time_minutes": 14.5,
            "prs_reviewed_this_week": 42
        },
        "heatmap": [
            {"developer": "alice", "security": 2, "performance": 1, "style": 5},
            {"developer": "bob", "security": 5, "performance": 3, "style": 2},
            {"developer": "charlie", "security": 0, "performance": 4, "style": 8}
        ],
        "accuracy": {
            "ai_suggested": 120,
            "human_accepted": 98,
            "acceptance_rate": "81.6%"
        }
    }
