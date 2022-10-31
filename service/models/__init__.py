from . import chunks, videos
from .models import BaseModel, db

BaseModel.metadata.create_all(db)
