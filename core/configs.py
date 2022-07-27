from pydantic import BaseSettings

from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:postgres@db:5432/postgres'
    DBBaseModel = declarative_base()

    JWT_SECRET: str = '2V2TFQeCw3UnKdTpd6QkQc_t9uWj6euPHbTz-tAaqUs'
    ALGORITH: str = 'HS256'
    # 60 minutos * 24 horas * 7 dias => 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True

settings: Settings = Settings()