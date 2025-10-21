from pydantic import BaseModel
from datetime import datetime
from app.schemas.users import UserOut


class PostBase(BaseModel):
    name: str
    content: str
    is_published: bool


class PostIn(PostBase):
    pass


class PostOut(PostBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    owner: UserOut

    class Config:
        from_attributes = True


class PostOutWithVotes(BaseModel):
    Post: PostOut
    votes: int

    class Config:
        from_attributes = True
