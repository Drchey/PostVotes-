# routes.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import posts as schema_post
from typing import List
from app.router import oauth2
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("", status_code=200, response_model=List[schema_post.PostOutWithVotes])
async def get_posts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 24,
    search: str | None = None,
):
    # Base query joining Posts and Votes
    query = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
    )

    # Apply search filter only if search is provided
    if search:
        query = query.filter(models.Post.name.ilike(f"%{search}%"))

    # Apply pagination
    results = query.order_by(models.Post.id.desc()).limit(limit).offset(skip).all()

    return results


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=List[schema_post.PostOut],
)
async def get_posts_from_user(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
    skip: int = 0,
    limit: int = 24,
    search: str | None = None,
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.user_id == current_user.id)
        .filter(models.Post.name.contains(search))
        .offset(skip)
        .limit(limit)
        .all()
    )

    return posts


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=schema_post.PostOut
)
async def create_post(
    post: schema_post.PostIn,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    new_post = models.Post(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schema_post.PostOut)
async def get_posts_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found"
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found"
        )
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    db.delete(post)
    db.commit()


@router.put(
    "/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schema_post.PostOut
)
async def update_post_by_id(
    id: int,
    post: schema_post.PostIn,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    exist_post = db.query(models.Post).filter(models.Post.id == id).first()
    if exist_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found"
        )
    if exist_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    for key, value in post.model_dump().items():
        setattr(exist_post, key, value)

    db.commit()
    db.refresh(exist_post)
    return exist_post
