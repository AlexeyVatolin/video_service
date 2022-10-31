from sqlalchemy import Column, ForeignKey, Integer, String

from ..models.videos import Video
from .models import BaseModel


class Chunk(BaseModel):
    __tablename__ = "chunk"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_second = Column(Integer)
    duration = Column(Integer)
    video_id = Column(Integer, ForeignKey(Video.id), primary_key=True)
    path = Column(String)

    exclude_fields = {"video_id"}

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in self.exclude_fields}

