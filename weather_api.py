import openmeteo_requests
import requests_cache
from retry_requests import retry

url = "https://api.open-meteo.com/v1/forecast"
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


async def get_weather_data(coordinates):
    params = {
        "latitude": coordinates.lat,
        "longitude": coordinates.lon,
        "current": ["temperature_2m", "surface_pressure", "wind_speed_10m"],
        "wind_speed_unit": "ms",
        "timezone": "Europe/Moscow"
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_surface_pressure = current.Variables(1).Value()
    current_wind_speed_10m = current.Variables(2).Value()

    return {
        "temperature_2m": current_temperature_2m,
        "surface_pressure": current_surface_pressure,
        "wind_speed_10m": current_wind_speed_10m
    }
