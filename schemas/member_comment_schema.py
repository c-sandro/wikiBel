from typing import Optional

from pydantic import BaseModel, EmailStr

class MemberCommentSchema(BaseModel):
    id: Optional[int] = None
    member_id: int
    monument_id: int
    comment: str

    class Config:
        orm_mode = True