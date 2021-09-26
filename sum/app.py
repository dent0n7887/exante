from aiohttp import web
from settings.settings import Settings
from utils.AppMiddleware import error_middleware
from consts import (
    DB_SESSION,
    SETTINGS,
    DATA_SERVICE
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import BaseModel, DataModel
from dao import DataDAO
from services import DataService

# Main app instance creation
app = web.Application()

# Settings singleton initialization
settings = Settings()
app[SETTINGS] = settings

# DAO initialization
data_dao = DataDAO(app)

# Service initialization
app[DATA_SERVICE] = DataService(data_dao=data_dao)

# Middleware
app.middlewares.append(error_middleware)

# DB engine initialization
engine = create_async_engine(
    f"postgresql+asyncpg://"
    f"{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}/{settings.DB_NAME}",
    echo="debug",
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
app[DB_SESSION] = session


def get_app():
    return app
