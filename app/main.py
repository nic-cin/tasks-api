from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables
from app import models  # noqa: F401
from app.routers import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Tasks API", version="0.3.0", lifespan=lifespan)
app.include_router(tasks.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Tasks API rodando"}