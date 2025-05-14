from typing import Optional

from pydantic import BaseModel, EmailStr

class MonumentSchema(BaseModel):
    id: Optional[int] = None
    member_id: int
    route: str
    route_time: str

    class Config:
        orm_mode = True