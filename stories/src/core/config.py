import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import SettingsConfigDict, BaseSettings

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class ProjectSettings(BaseSettings):
    url_prefix: str = ""

    debug: bool = Field(False)

    # authjwt_secret_key: str = Field(..., alias="JWT_ACCESS_TOKEN_SECRET_KEY")

    model_config = SettingsConfigDict(env_prefix='project_', env_file='.env', extra='ignore')

class PostgresSettings(BaseSettings):
    stories_db: str = Field('stories')
    user: str = ...
    password: str = ...
    host: str = Field('localhost')
    port: int = Field(5432)
    echo: bool = Field(True)
    dbschema: str = Field('public')

    model_config = SettingsConfigDict(env_prefix='postgres_', env_file='.env', extra='ignore')

    def get_dsn(self):
        return f'postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.stories_db}'

    def get_connection_info(self):
        return {
            'url': self.get_dsn(),
            'connect_args': {'options': f"-c search_path={self.dbschema},public"}
        }

class GunicornSettings(BaseSettings):
    host: str = Field('0.0.0.0')
    port: int = Field(8000)
    workers: int = Field(2)
    loglevel: str = Field('debug')
    model_config = SettingsConfigDict(env_prefix='gunicorn_', env_file='.env', extra='ignore')

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

project_settings = ProjectSettings()
postgres_settings = PostgresSettings()
gunicorn_settings =GunicornSettings()