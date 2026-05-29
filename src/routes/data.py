from fastapi import Depends, FastAPI , APIRouter ,UploadFile
import os
from helpers.config import get_settings, Settings
from controllers import DataController

data_router = APIRouter(
    prefix = "/api/v1/data",
    tags = ['api_v1','data']
)

@data_router.post("/process/{project_id}")
async def process_data(project_id: str, file: UploadFile,
                    settings: Settings = Depends(get_settings)):
    
    is_valid , message = DataController().is_valid_file(file = file)
    if not is_valid:
        return {"error": message}
    else:
        # Here you would add your file processing logic
        return {"message": "File is valid and ready for processing."}