from http import HTTPStatus
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db import Base, engine, get_async_session
from models import User, City  # noqa
from schemas import Coordinates, UserCreate, UserDB, CityCreate
from services import update_weather_for_all_cities, get_weather_for_city
from crud import user_crud, city_crud
from weather_api import get_temperature_pressure_windspeed

app = FastAPI(
    title=settings.app_title,
    description=settings.description
)

scheduler = AsyncIOScheduler()


def start_weather_update_task(session: AsyncSession):
    scheduler.add_job(
        update_weather_for_all_cities,
        'interval',
        minutes=15,
        args=[session]
    )
    scheduler.start()


@app.on_event("startup")
async def startup_event():
    async_session = get_async_session()
    session = await async_session.__anext__()
    start_weather_update_task(session)


@app.get('/')
def read_root():
    return {'weather_info': 'hello!'}


@app.post("/weather")
async def get_weather(coordinates: Coordinates):
    return await get_temperature_pressure_windspeed(coordinates)


@app.post('/register', response_model=UserDB)
async def register_user(
        data: UserCreate,
        session: AsyncSession = Depends(get_async_session)):
    return await user_crud.create(data, session)


@app.post('/add-city')
async def add_city(
        city: CityCreate,
        session: AsyncSession = Depends(get_async_session)):
    city = await city_crud.create(city, session)
    await get_weather_for_city(session, city)
    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content={'message': 'Город добавлен в отслеживаемые'}
    )


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())
    uvicorn.run('script:app', reload=True)
