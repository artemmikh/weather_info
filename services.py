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

        city.temperature_max = daily_weather["temperature_max"][0]
        city.temperature_min = daily_weather["temperature_min"][0]
        city.precipitation_sum = daily_weather["precipitation_sum"][0]
        city.precipitation_hours = daily_weather["precipitation_hours"][0]
        city.wind_speed_max = daily_weather["wind_speed_max"][0]


async def update_weather_for_all_cities(session: AsyncSession) -> None:
    result = await session.execute(select(City))
    cities = result.scalars().all()
    await update_weather(cities)
    await session.commit()


async def get_weather_for_city(session: AsyncSession, city: City):
    await update_weather([city])
