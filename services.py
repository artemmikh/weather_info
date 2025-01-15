from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import City
from schemas import Coordinates
from weather_api import get_current_weather_for_update


async def update_weather(session: AsyncSession, cities: list[City]) -> None:
    for city in cities:
        coordinates = Coordinates(lat=city.lat, lon=city.lon)
        current_weather = await get_current_weather_for_update(coordinates)
        for key, value in current_weather.items():
            setattr(city, key, value)
        await session.commit()


async def update_weather_for_all_cities(session: AsyncSession):
    cities = await session.execute(select(City))
    cities = cities.scalars().all()
    await update_weather(session, cities)


async def get_weather_for_city(session: AsyncSession, city: City):
    await update_weather(session, [city])
