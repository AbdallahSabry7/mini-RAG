from fastapi import FastAPI , APIRouter
from dotenv import load_dotenv
import os

base_router = APIRouter( prefix = "/api/v1" , tags =['api_v1'])

load_dotenv()

@base_router.get("/")
async def default():
    app_name = os.getenv('APP_NAME')
    app_version = os.getenv('APP_VERSION')
    app_description = os.getenv('APP_DESCRIPTION')
    return {'message': f"Welcome to the {app_name} API!", 'version': app_version, 'description': app_description}