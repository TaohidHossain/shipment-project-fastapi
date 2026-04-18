from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import URL
from sqlmodel import SQLModel

from app.config import settings

DB_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_SERVER,
    port=int(settings.POSTGRES_PORT),
    database=settings.POSTGRES_DATABASE,
).render_as_string(hide_password=False)

engine = create_async_engine(
    url= DB_URL,
    echo= bool(settings.DEBUG)
)

async def create_db_tables():
    try:
        async with engine.begin() as connection:
            from app.database.models import Shipment, Seller
            await connection.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        raise RuntimeError(f"Failed to create tables: {e}")

async_session = sessionmaker(
        bind=engine, # type: ignore
        class_=AsyncSession,
        expire_on_commit=False
    ) # type: ignore

async def get_session():
    async with async_session() as session: # type: ignore
        yield session
