from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from core.configs import settings

class MonumentTypeModel(settings.DBBaseModel):
    __tablename__ = 'monument_type'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    monument_type: str = Column(String(45), nullable=False)

    monument = relationship("MonumentModel")