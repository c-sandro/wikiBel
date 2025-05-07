from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings

class MemberModel(settings.DBBaseModel):
    __tablename__ = 'member'

    id_u: int = Column(Integer, primary_key=True, autoincrement=True)
    name_u: str = Column(String(256), nullable=False)
    email_u: str = Column(String(256), nullable=False, unique=True)
    password_u: str = Column(String(256), nullable=False)
    is_premium_u: bool = Column(Boolean, default=False, nullable=False)
    token_u: str = Column(String(36), nullable=False, unique=True)