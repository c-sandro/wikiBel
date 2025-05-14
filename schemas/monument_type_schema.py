from typing import Optional

from pydantic import BaseModel, EmailStr

class MonumentSchema(BaseModel):
    id: Optional[int] = None
    monument_type: str

    class Config:
        orm_mode = True