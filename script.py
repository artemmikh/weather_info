import asyncio
from asyncio import wait_for
from http import HTTPStatus
from typing import List, Literal

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import uvicorn
from fastapi import FastAPI, Depends, logger
from fastapi.params import Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db import Base, engine, get_async_session, AsyncSessionLocal
from models import User, City  # noqa
from schemas import Coordinates, UserCreate, UserDB, CityCreate, CityDB, \
    WeatherResponse
from services import update_weather_for_all_cities, get_weather_for_city
from crud import user_crud, city_crud
from validators import check_user_name_duplicate, check_city_name_duplicate, \
    check_city_exists, check_time
from weather_api import get_temperature_pressure_windspeed, \
    get_today_weather_by_time

app = FastAPI(
    title=settings.app_title,
    description=settings.description
)


async def update_weather_periodically(session):
    while True:
        settings.logger.info('Запущен процесс периодического обновления '
                             'погоды для отслеживаемых городов.')
        await update_weather_for_all_cities(session)
        await asyncio.sleep(settings.update_interval_seconds)


@app.on_event("startup")
async def startup():
    async for session in get_async_session():
        loop = asyncio.get_event_loop()
        loop.create_task(update_weather_periodically(session))


@app.get('/')
def read_root():
    return {'weather_info': 'hello!'}


@app.post("/weather")
async def get_weather_by_coordinates(coordinates: Coordinates):
    return await get_temperature_pressure_windspeed(coordinates)


@app.get(
    "/weather",
    response_model=WeatherResponse,
    response_model_exclude_none=True,
)
async def get_weather_by_time(
        city: str,
        hour: int = Query(
            ...,
            ge=0, le=23,
            description="Время в формате от 0 до 23, "
                        "где 0 — это полночь, а 23 — 23:00"
        ),
        params: List[Literal[
            "temperature", "humidity", "wind_speed", "precipitation"]] = Query(
            ...,
            description="Параметры погоды, которые необходимо вернуть. "
                        "Возможные значения: "
                        "temperature, humidity, wind_speed, precipitation."
        ),
        session: AsyncSession = Depends(get_async_session)
):
    await check_city_exists(city, session)
    await check_time(hour)
    city = await city_crud.get_city_obj_by_name(city, session)
    coordinates = Coordinates(lat=city.lat, lon=city.lon)
    weather = await get_today_weather_by_time(coordinates, hour)
    return {param: weather[param] for param in params if param in weather}


@app.post('/users', response_model=UserDB)
async def register_user(
        data: UserCreate,
        session: AsyncSession = Depends(get_async_session)):
    await check_user_name_duplicate(data.name, session)
    return await user_crud.create(data, session)


@app.post('/city')
async def add_city(
        city: CityCreate,
        session: AsyncSession = Depends(get_async_session)):
    await check_city_name_duplicate(city.name, session)
    city = await city_crud.create(city, session)
    await get_weather_for_city(session, city)
    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content={'message': 'Город добавлен в отслеживаемые'}
    )


@app.get('/city', response_model=list[CityDB])
async def get_list_city(session: AsyncSession = Depends(get_async_session)):
    return await city_crud.get_multi(session)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(create_tables())
    uvicorn.run('script:app', reload=True)
