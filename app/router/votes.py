from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.schemas import votes as schema_votes
from app.router.oauth2 import get_current_user
from app.database import get_db
from app import models

router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def vote(
    vote: schema_votes.Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=400, detail="Already voted")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added"}
    else:
        if not found_vote:
            raise HTTPException(status_code=404, detail="Vote not found")
        db.delete(found_vote)  # ✅ delete the instance, not the query
        db.commit()
        return {"message": "Vote removed"}
