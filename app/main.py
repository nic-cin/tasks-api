from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables
from app import models  # noqa: F401  (garante que Task seja registrado antes do create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Tasks API", version="0.2.0", lifespan=lifespan)


@app.get("/")
def root():
    return {"status": "ok", "message": "Tasks API rodando"}