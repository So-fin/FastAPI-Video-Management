# models.py
from sqlalchemy import Column, Integer, String, Float
from database import Base, engine


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    size = Column(Float)
    format = Column(String)
    path = Column(String)

