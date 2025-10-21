from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from typing import List
from app.schemas import users as schema_users
from sqlalchemy.exc import IntegrityError
from app.utils import get_password_hash


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=List[schema_users.UserOut]
)
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=schema_users.UserOut
)
async def register_user(user: schema_users.UserIn, db: Session = Depends(get_db)):
    user.password = get_password_hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    return new_user


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schema_users.UserOut
)
async def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} is not found",
        )
    return user
