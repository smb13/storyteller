from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.routers import all_v1_routers
from core.config import postgres_settings, project_settings
from db import alchemy
from db.alchemy import create_database


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    dsn = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}".format(
        user=postgres_settings.user,
        password=postgres_settings.password,
        host=postgres_settings.host,
        port=postgres_settings.port,
        db_name=postgres_settings.dbname,
    )
    alchemy.engine = create_async_engine(dsn, echo=True, future=True)
    alchemy.AsyncSessionLocal = sessionmaker(alchemy.engine, class_=AsyncSession, expire_on_commit=False)

    # Импорт моделей необходим для их автоматического создания
    from models import User  # noqa

    if project_settings.debug:
        await create_database()

    yield


# @AuthJWT.load_config
# def get_config() -> object:
#     return project_settings


app = FastAPI(
    title="API для получения ",
    version="1.0.0",
    docs_url=project_settings.url_prefix + "/api/openapi",
    redoc_url=project_settings.url_prefix + "/api/redoc",
    openapi_url=project_settings.url_prefix + "/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


app.include_router(all_v1_routers)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
    )