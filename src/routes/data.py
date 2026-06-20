from fastapi import Depends, FastAPI , APIRouter ,UploadFile , status
from fastapi.responses import JSONResponse
import os

from helpers.config import get_settings, Settings
from controllers import DataController , ProjectController , ProcessController
import aiofiles
import models
import logging
from .schemas import processData

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
    
    folder_path = ProjectController().get_file_path(project_id = project_id)
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

    return JSONResponse(status_code=status.HTTP_200_OK, content={'signal' : models.ResponseStatus.File_Upload_Success.value,
                        'file_id': filename})
    

@data_router.post("/process_file/{project_id}")
async def process_file(project_id: str, data: processData):
    file_id = data.file_id
    chunk_size = data.chunk_size
    overlap = data.overlap

    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(project_id=project_id, filename=file_id)
    chunks = process_controller.process_file_content(file_content=file_content, file_id=file_id,
                                                        chunk_size=chunk_size, chunk_overlap=overlap)
    
    if chunks is None or len(chunks) == 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"signal": models.ResponseStatus.File_processing_failed.value})
    else:
        return chunks