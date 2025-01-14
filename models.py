from sqlalchemy import Column, String, Float

from core.db import Base


class User(Base):
    name = Column(String(100), unique=True, nullable=False)


class City(Base):
    name = Column(String(100), unique=True, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
