from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings

class MemberCommentModel(settings.DBBaseModel):
    __tablename__ = 'member_comment'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    member_id: int = Column(Integer, ForeignKey('member.id'), nullable=False)
    monument_id: int = Column(Integer, ForeignKey('monument.id'), nullable=False)
    comment: str = Column(String(500), nullable=False)

    member = relationship("MemberModel", back_populates="member_comment")
    monument = relationship("MonumentModel", back_populates="member_comment")