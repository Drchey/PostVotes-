from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, utils
from app.router import oauth2
from datetime import timedelta
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.schemas import token
from app.config import settings

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["auth"], prefix="")


@router.post("/login", status_code=status.HTTP_200_OK, response_model=token.Token)
async def login(
    user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = (
        db.query(models.User).filter(models.User.email == user_creds.username).first()
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
        )
    if not utils.verify_password(user_creds.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
        )

    # Create Token
    access_token = oauth2.create_access_token(
        data={"user_id": user.id, "sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    # Return Token
    return {"access_token": access_token, "token_type": "bearer"}
