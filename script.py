import uvicorn
from fastapi import FastAPI

from core.config import settings
from core.db import Base, engine
from models import User, City  # noqa
from schemas import Coordinates
from weather_api import get_weather_data

app = FastAPI(
    title=settings.app_title,
    description=settings.description
)


@app.get('/')
def read_root():
    return {'weather_info': 'hello!'}


@app.post("/weather")
async def get_weather(coordinates: Coordinates):
    return await get_weather_data(coordinates)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())
    uvicorn.run('script:app', reload=True)
