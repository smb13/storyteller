from fastapi import APIRouter

from core.config import postgres_settings

API_PREFIX_V1 = postgres_settings.url_prefix + "/api/v1"

all_v1_routers = APIRouter(prefix=API_PREFIX_V1)