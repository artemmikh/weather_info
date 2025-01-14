from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Weather info'
    database_url: str = 'sqlite+aiosqlite:///./weather.db'
    description: str = 'HTTP-сервер для предоставления информации по погоде'

    class Config:
        env_file = '.env'


settings = Settings()
