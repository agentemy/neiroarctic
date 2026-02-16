from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.database import init_models, async_engine
from db.data_extraction import get_all_physiological_by_individual

@asynccontextmanager
async def lifespan(app):
    init_models()
    yield
    await async_engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def func():
    return {"Hello": "World"}

@app.get("/metrics/{ind_num}")
async def metrics(ind_num: str):
    return await get_all_physiological_by_individual(ind_num)

