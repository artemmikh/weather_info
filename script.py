import asyncio
from http import HTTPStatus
from typing import List, Literal

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.params import Query
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db import Base, engine, get_async_session
from crud import city_crud
from models import City  # noqa
from schemas import Coordinates, CityCreate, CityDB, WeatherResponse
from services import update_weather_for_all_cities, get_weather_for_city
from validators import check_city_name_duplicate, check_city_exists, check_time
from weather_api import get_temperature_pressure_windspeed, \
    get_today_weather_by_hour

app = FastAPI(
    title=settings.app_title,
    description=settings.description
)


async def update_weather_periodically(session: AsyncSession) -> None:
    """Периодически обновляет погоду для всех отслеживаемых городов."""
    while True:
        settings.logger.info('Запущен процесс периодического обновления '
                             'погоды для отслеживаемых городов.')
        await update_weather_for_all_cities(session)
        await asyncio.sleep(settings.update_interval_seconds)


@app.on_event('startup')
async def startup() -> None:
    """Запускает процесс обновления погоды при старте приложения."""
    async for session in get_async_session():
        loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        loop.create_task(update_weather_periodically(session))


@app.get('/')
def read_root() -> RedirectResponse:
    return RedirectResponse(url='/docs')


@app.post('/weather')
async def get_current_weather_by_coordinates(
        coordinates: Coordinates
) -> dict[str, float]:
    """Получает текущую погоду по координатам."""
    return await get_temperature_pressure_windspeed(coordinates)


@app.get(
    '/weather',
    response_model=WeatherResponse,
    response_model_exclude_none=True,
)
async def get_today_weather_by_time(
        city: str,
        hour: int = Query(
            ...,
            ge=0, le=23,
            description='Время в формате от 0 до 23, '
                        'где 0 — это полночь, а 23 — 23:00'
        ),
        params: List[Literal[
            'temperature', 'humidity', 'wind_speed', 'precipitation']] = Query(
            ...,
            description='Параметры погоды, которые необходимо вернуть. '
                        'Возможные значения: '
                        'temperature, humidity, wind_speed, precipitation.'
        ),
        session: AsyncSession = Depends(get_async_session)
) -> dict[str, float]:
    """Получает погоду по заданному городу и часу."""
    await check_city_exists(city, session)
    await check_time(hour)
    city_obj = await city_crud.get_city_obj_by_name(city, session)
    coordinates = Coordinates(lat=city_obj.lat, lon=city_obj.lon)
    weather = await get_today_weather_by_hour(coordinates, hour)
    return {param: weather[param] for param in params if param in weather}


@app.post('/city')
async def add_city(
        city: CityCreate,
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    """Добавляет город в отслеживаемые города и обновляет для него прогноз."""
    await check_city_name_duplicate(city.name, session)
    city_obj = await city_crud.create(city, session)
    await get_weather_for_city(city_obj, session)
    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content={'message': 'Город добавлен в отслеживаемые'}
    )


@app.get('/city', response_model=list[CityDB])
async def get_list_city(
        session: AsyncSession = Depends(get_async_session)
) -> list[CityDB]:
    """Возвращает список отслеживаемых городов."""
    return await city_crud.get_multi(session)


async def create_tables() -> None:
    """Создает таблицы в базе данных."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(create_tables())
    uvicorn.run('script:app', reload=True)
