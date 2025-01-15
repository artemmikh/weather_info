from typing import Optional

from pydantic import BaseModel


class Coordinates(BaseModel):
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
    id: int
    name: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str

    class Config:
        schema_extra = {
            'example': {
                'name': 'Иван',
            }
        }


class UserDB(BaseModel):
    id: int

    class Config:
        orm_mode = True


class WeatherResponse(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    precipitation: Optional[float] = None
