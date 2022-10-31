from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tornado.options import options

db = create_engine(options.database_url)
BaseModel = declarative_base()
DBSession = sessionmaker(bind=db)
