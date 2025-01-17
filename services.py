from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from crud import city_crud
from models import City
from schemas import Coordinates, CityUpdate
from weather_api import get_daily_weather


async def update_weather(cities: list[City]) -> None:
    for city in cities:
        coordinates = Coordinates(lat=city.lat, lon=city.lon)
        daily_weather = await get_daily_weather(coordinates)

        for key, value in daily_weather.items():
            if value is not None and hasattr(city, key):
                setattr(city, key, value[0])


async def update_weather_for_all_cities(session: AsyncSession) -> None:
    result = await session.execute(select(City))
    cities = result.scalars().all()
    await update_weather(cities)
    await session.commit()


async def get_weather_for_city(session: AsyncSession, city: City):
    await update_weather([city])
