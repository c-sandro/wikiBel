from typing import Optional

from pydantic import BaseModel, EmailStr

class MonumentSchema(BaseModel):
    id: Optional[int] = None
    name: str
    type_id: int
    longitude: float
    latitude: float
    founding_year: int
    district: str
    description: str
    open_hours: str

    class Config:
        orm_mode = True