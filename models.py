from sqlalchemy import Column, String, Float

from core.db import Base


class User(Base):
    name = Column(String(100), unique=True, nullable=False)


class City(Base):
    name = Column(String(100), unique=True, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    temperature_max = Column(Float)  # Максимальная температура
    temperature_min = Column(Float)  # Минимальная температура
    precipitation_sum = Column(Float)  # Сумма осадков
    precipitation_hours = Column(Float)  # Часы осадков
    wind_speed_max = Column(Float)  # Максимальная скорость ветра
