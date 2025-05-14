from typing import Optional

from pydantic import BaseModel, EmailStr

class MemberSchemaBase(BaseModel):
    id_u: Optional[int] = None
    name_u: str
    email_u: EmailStr

    class Config:
        orm_mode = True

#Essas classes são criadas pra não enviar a senha desnecessariamente e arriscar quebrar criptografia
class MemberSchemaCreated(MemberSchemaBase):
    password_u: str
    token_u: str

class MemberSchemaUpdated(MemberSchemaBase):
    name_u: Optional[str]
    email_u: Optional[EmailStr]
    password_u: Optional[str]
    is_premium_u: Optional[bool]