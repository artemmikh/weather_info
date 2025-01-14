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


class City(BaseModel):
    name: str
    coordinates: Coordinates


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
