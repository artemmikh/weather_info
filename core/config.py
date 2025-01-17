import logging

from pydantic import BaseSettings

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
)
logger: logging.Logger = logging.getLogger()


class Settings(BaseSettings):
    app_title: str = 'Weather info'
    database_url: str = 'sqlite+aiosqlite:///./weather.db'
    description: str = 'HTTP-сервер для предоставления информации по погоде'
    update_interval_seconds: int = 900
    logger: logging.Logger = logger
    open_meteo_url = 'https://api.open-meteo.com/v1/forecast'

    class Config:
        env_file: str = '.env'


settings = Settings()
