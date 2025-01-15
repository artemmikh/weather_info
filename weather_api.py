from datetime import datetime
from http import HTTPStatus

import openmeteo_requests
import requests_cache
from fastapi import HTTPException
from openmeteo_sdk.VariablesWithTime import VariablesWithTime
from retry_requests import retry

from schemas import Coordinates

url = "https://api.open-meteo.com/v1/forecast"
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


async def get_current_weather(coordinates: Coordinates) -> VariablesWithTime:
    params: dict = {
        "latitude": coordinates.lat,
        "longitude": coordinates.lon,
        "current": [
            "temperature_2m",
            "surface_pressure",
            "wind_speed_10m",
            "relative_humidity_2m",
            'precipitation',
        ],
        "wind_speed_unit": "ms",
        "timezone": "Europe/Moscow"
    }
    try:
        responses = openmeteo.weather_api(url, params=params)
        return responses[0].Current()
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail=f'Ошибка получения данных от {url}',
        )


async def get_temperature_pressure_windspeed(coordinates: Coordinates) -> dict:
    current: VariablesWithTime = await get_current_weather(coordinates)
    return {
        "temperature_2m": current.Variables(0).Value(),
        "surface_pressure": current.Variables(1).Value(),
        "wind_speed_10m": current.Variables(2).Value()
    }


async def get_current_weather_for_update(coordinates: Coordinates) -> dict:
    current: VariablesWithTime = await get_current_weather(coordinates)
    return {
        "temperature": current.Variables(0).Value(),
        "humidity": current.Variables(1).Value(),
        "precipitation": current.Variables(2).Value(),
        "wind_speed": current.Variables(3).Value()
    }


async def get_today_weather_by_time(coordinates: Coordinates,
                                    hour: int) -> dict:
    pass
