from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from core.configs import settings

class MonumentModel(settings.DBBaseModel):
    __tablename__ = 'monument'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(100), nullable=False)
    type_id: int = Column(Integer, ForeignKey('monument_type.id'), nullable=False)
    longitude: str = Column(String(45))
    latitude: str = Column(String(45))
    founding_year: int = Column(Integer, nullable=False)
    district: str = Column(String(50), nullable=False)
    description: str = Column(Text, nullable=False)
    open_hours: str = Column(String(300), nullable=False)

    member_comment = relationship("MemberCommentModel", back_populates="monument")
    monument_type = relationship("MonumentTypeModel", back_populates="monument")