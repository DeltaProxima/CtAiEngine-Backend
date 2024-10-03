from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from database import Base
from sqlalchemy.sql import func
from database import engine

class RoadImages(Base):
    __tablename__ = "road_images"
    id = Column(Integer, primary_key=True, index=True)
    road_image = Column(String)
    latitude = Column(String)
    longitude = Column(String)

Base.metadata.create_all(bind=engine)