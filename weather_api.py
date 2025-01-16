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


async def get_openmeteo_response(params: dict):
    try:
        responses = openmeteo.weather_api(url, params=params)
        return responses
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail=f'Ошибка получения данных от {url}',
        )


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
    responses = await get_openmeteo_response(params)
    return responses[0].Current()


async def get_temperature_pressure_windspeed(coordinates: Coordinates) -> dict:
    current: VariablesWithTime = await get_current_weather(coordinates)
    return {
        "temperature_2m": current.Variables(0).Value(),
        "surface_pressure": current.Variables(1).Value(),
        "wind_speed_10m": current.Variables(2).Value()
    }


async def get_daily_weather(coordinates: Coordinates) -> dict:
    """
    Получает ежедневный прогноз погоды для заданных координат.
    """
    params = {
        "latitude": coordinates.lat,
        "longitude": coordinates.lon,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "precipitation_hours",
            "wind_speed_10m_max"
        ],
        "timezone": "Europe/Moscow"
    }
    responses = await get_openmeteo_response(params)
    response = responses[0]
    daily = response.Daily()
    return {
        "temperature_max": daily.Variables(0).ValuesAsNumpy().tolist(),
        "temperature_min": daily.Variables(1).ValuesAsNumpy().tolist(),
        "precipitation_sum": daily.Variables(2).ValuesAsNumpy().tolist(),
        "precipitation_hours": daily.Variables(3).ValuesAsNumpy().tolist(),
        "wind_speed_max": daily.Variables(4).ValuesAsNumpy().tolist(),
    }


async def get_today_weather_by_time(coordinates: Coordinates,
                                    hour: int) -> dict:
    params = {
        "latitude": coordinates.lat,
        "longitude": coordinates.lon,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m"
        ],
        "timezone": "GMT",
        "forecast_days": 1
    }
    responses = await get_openmeteo_response(params)
    response = responses[0]
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(3).ValuesAsNumpy()

    return {
        'temperature': hourly_temperature_2m[hour].item(),
        'precipitation': hourly_precipitation[hour].item(),
        'humidity': hourly_relative_humidity_2m[hour].item(),
        'wind_speed': hourly_wind_speed_10m[hour].item()
    }
