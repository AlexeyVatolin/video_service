from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .models import BaseModel


class Video(BaseModel):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    chunk = relationship("Chunk", order_by="Chunk.id")

    def as_dict(self, with_related: bool = False):
        result = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if with_related:
            for field in self.__mapper__.relationships:
                result[field.key] = [x.as_dict() for x in getattr(self, field.key)]
        return result
