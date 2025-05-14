from typing import Optional

from pydantic import BaseModel, EmailStr

class MemberSchemaBase(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

#Essas classes são criadas pra não enviar a senha desnecessariamente e arriscar quebrar criptografia
class MemberSchemaCreated(MemberSchemaBase):
    password: str
    token: str

class MemberSchemaUpdated(MemberSchemaBase):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_premium: Optional[bool]