from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from core.configs import settings

class RouteModel(settings.DBBaseModel):
    __tablename__ = 'route'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    member_id: int = Column(Integer, ForeignKey('member.id'), nullable=False)
    route: str = Column(Text, nullable=False)
    route_time: str = Column(String(15))
    member = relationship("MemberModel", back_populates="route")