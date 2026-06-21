from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.review_router import router as review_router
from app.api.auth_router import router as auth_router
from app.core.config import settings
from app.db.session import engine, Base
import app.models.user
import app.models.review

# Create tables (for local development)
Base.metadata.create_all(bind=engine)

from app.api.webhook_router import router as webhook_router
from app.api.ws_router import router as ws_router
from app.api.analytics_router import router as analytics_router

app = FastAPI(title=settings.PROJECT_NAME)

# Enable CORS for local Next.js client development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(review_router, prefix="/api")
app.include_router(auth_router, prefix="/auth/github")
app.include_router(webhook_router, prefix="/api/webhooks/github")
app.include_router(ws_router, prefix="/api/ws")
app.include_router(analytics_router, prefix="/api/analytics")

@app.get("/")
def root():
    return {"message": f"{settings.PROJECT_NAME} Backend Running"}