import os
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.core.security import create_access_token

router = APIRouter()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

@router.get("/login")
def login_github():
    if not GITHUB_CLIENT_ID:
        raise HTTPException(status_code=500, detail="GITHUB_CLIENT_ID not configured")
    github_auth_url = f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&scope=user:email"
    return RedirectResponse(github_auth_url)

@router.get("/callback")
async def auth_callback(code: str, db: Session = Depends(get_db)):
    if not code:
        raise HTTPException(status_code=400, detail="Code not provided")
        
    async with httpx.AsyncClient() as client:
        # Exchange code for access token
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
            }
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to authenticate with GitHub")
            
        # Get user info
        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_data = user_response.json()
        
        github_id = str(user_data.get("id"))
        username = user_data.get("login")
        email = user_data.get("email")
        
        if not email:
            # Try to fetch emails if not public
            email_resp = await client.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            emails = email_resp.json()
            if isinstance(emails, list) and len(emails) > 0:
                primary_email = next((e["email"] for e in emails if e["primary"]), None)
                email = primary_email or emails[0]["email"]

        # Upsert user
        user = db.query(User).filter(User.github_id == github_id).first()
        if not user:
            user = User(github_id=github_id, username=username, email=email)
            db.add(user)
            db.commit()
            db.refresh(user)
            
        # Generate JWT
        jwt_token = create_access_token({"sub": str(user.id)})
        
        # Redirect to frontend with token
        return RedirectResponse(f"{FRONTEND_URL}/?token={jwt_token}")
