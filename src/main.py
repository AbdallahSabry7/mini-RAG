from fastapi import FastAPI
from routes import base_router, data_router
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URl)
    app.state.mongodb_database = app.state.mongodb_client[settings.MONGODB_DATABASE]
    yield
    app.state.mongodb_client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(base_router)
app.include_router(data_router)




