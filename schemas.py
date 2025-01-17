from typing import Optional
from pydantic import BaseModel


class Coordinates(BaseModel):
    """Схема географических координат города"""
    lat: float
    lon: float

    class Config:
        schema_extra = {
            'example': {
                'lat': '59.93903',
                'lon': '30.315759',
            }
        }


class CityCreate(BaseModel):
    """Схема данных для создания нового города"""
    name: str
    lat: float
    lon: float

    class Config:
        schema_extra = {
            'example': {
                'name': 'Moscow',
                'lat': '55.7522',
                'lon': '37.6156',
            }
        }


class CityDB(BaseModel):
    """Схема модели города в базе данных"""
    id: int
    name: str

    class Config:
        orm_mode = True


class CityUpdate(BaseModel):
    """Схема данных для обновления информации о погоде в городе"""
    temperature_max: Optional[float]
    temperature_min: Optional[float]
    precipitation_sum: Optional[float]
    precipitation_hours: Optional[float]
    wind_speed_max: Optional[float]


class UserCreate(BaseModel):
    """Схема данных для создания нового пользователя"""
    name: str

    class Config:
        schema_extra = {
            'example': {
                'name': 'Иван',
            }
        }


class UserDB(BaseModel):
    """Схема модели пользователя в базе данных"""
    id: int

    class Config:
        orm_mode = True


class WeatherResponse(BaseModel):
    """Схема ответа с данными о погоде для города"""
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    precipitation: Optional[float] = None
