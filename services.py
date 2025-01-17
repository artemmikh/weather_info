from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import City
from schemas import Coordinates
from weather_api import get_daily_weather


async def update_weather(cities: List[City]) -> None:
    for city in cities:
        coordinates: Coordinates = Coordinates(lat=city.lat, lon=city.lon)
        daily_weather: dict = await get_daily_weather(coordinates)

        for key, value in daily_weather.items():
            if value is not None and hasattr(city, key):
                setattr(city, key, value[0])


async def update_weather_for_all_cities(session: AsyncSession) -> None:
    result = await session.execute(select(City))
    cities: List[City] = result.scalars().all()
    await update_weather(cities)
    await session.commit()


async def get_weather_for_city(city: City) -> None:
    await update_weather([city])
