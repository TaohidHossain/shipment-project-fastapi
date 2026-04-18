from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.router import api_router
from app.database.session import create_db_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_tables()
    yield

app = FastAPI(
    lifespan=lifespan
)

app.include_router(api_router)