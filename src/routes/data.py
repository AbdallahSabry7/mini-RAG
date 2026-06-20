from fastapi import Depends, FastAPI , APIRouter ,UploadFile , status
from fastapi.responses import JSONResponse
import os

from helpers.config import get_settings, Settings
from controllers import DataController , ProcessController
import aiofiles
import models
import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix = "/api/v1/data",
    tags = ['api_v1','data']
)

@data_router.post("/process/{project_id}")
async def process_data(project_id: str, file: UploadFile,
                    settings: Settings = Depends(get_settings)):
    app_settings = get_settings()
    
    is_valid , message = DataController().is_valid_file(file = file)
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": message})
    
    folder_path = ProcessController().get_file_path(project_id = project_id)
    filename = DataController().generate_unique_filename(file.filename, project_id)
    file_location = os.path.join(folder_path, filename)

    while os.path.exists(file_location):
        filename = DataController().generate_unique_filename(file.filename, project_id)
        file_location = os.path.join(folder_path, filename)

    try:
        async with aiofiles.open(file_location, 'wb') as out_file:
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
                await out_file.write(chunk)
    except Exception as e:
        logger.error(f"Error occurred while saving the file: {str(e)}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=models.ResponseStatus.File_Upload_Failed.value)

    return JSONResponse(status_code=status.HTTP_200_OK, content= models.ResponseStatus.File_Upload_Success.value)
    