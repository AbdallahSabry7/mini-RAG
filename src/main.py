from fastapi import FastAPI
from routes import base_router, data_router
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager
from stores.LLM.LLMProviderFactory import LLMProviderFactory

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URl)
    app.state.mongodb_database = app.state.mongodb_client[settings.MONGODB_DATABASE]
    llm_factory = LLMProviderFactory(config=settings.dict())
    app.state.generation_client = llm_factory.create_provider(settings.GENERATION_BACKEND)
    app.state.generation_client.set_generator(settings.GENERATION_MODEL_ID)

    app.state.embedding_client = llm_factory.create_provider(settings.EMBEDDING_BACKEND)
    app.state.embedding_client.set_embedding(settings.EMBEDDING_MODEL_ID, settings.EMBEDDING_MODEL_SIZE)
    yield
    app.state.mongodb_client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(base_router)
app.include_router(data_router)




