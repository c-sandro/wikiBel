from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings

class MemberModel(settings.DBBaseModel):
    __tablename__ = 'member'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(256), nullable=False)
    email: str = Column(String(256), nullable=False, unique=True)
    password: str = Column(String(256), nullable=False)
    is_premium: bool = Column(Boolean, default=False, nullable=False)
    token: str = Column(String(36), nullable=False, unique=True)

    member_comment = relationship("MemberCommentModel", back_populates="member")
    route = relationship("RouteModel", back_populates="member")