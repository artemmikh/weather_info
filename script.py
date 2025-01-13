import uvicorn
from fastapi import FastAPI

from schemas import Coordinates
from weather_api import get_weather_data

app = FastAPI()


@app.get('/')
def read_root():
    return {'weather_info': 'hello!'}


@app.post("/weather")
async def get_weather(coordinates: Coordinates):
    return await get_weather_data(coordinates)


if __name__ == '__main__':
    uvicorn.run('script:app', reload=True)
