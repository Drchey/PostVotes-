from pydantic import BaseModel, field_validator


class Vote(BaseModel):
    post_id: int
    # user_id: int
    dir: int  # 0 = remove vote, 1 = add vote

    @field_validator("dir")
    @classmethod
    def validate_dir(cls, v):
        if v not in (0, 1):
            raise ValueError("dir must be 0 or 1")
        return v
