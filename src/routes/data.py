from bson import ObjectId
from fastapi import Depends, FastAPI , APIRouter ,UploadFile , status , Request
from fastapi.responses import JSONResponse
import os
from models.projectModel import ProjectModel
from models.chunkModel import ChunkModel
from helpers.config import get_settings, Settings
from controllers import DataController , ProjectController , ProcessController
import aiofiles
import models
import logging
from .schemas import processData 
from models.db_schemas import DataChunk

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix = "/api/v1/data",
    tags = ['api_v1','data']
)

@data_router.post("/process/{project_id}")
async def process_data(req: Request, project_id: str, file: UploadFile,
                    settings: Settings = Depends(get_settings)):
    app_settings = get_settings()
    
    project_model = await ProjectModel.create_instance(
        db_conn=req.app.state.mongodb_database
    )

    project = await project_model.get_project_or_create(project_id=project_id)

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
                        'file_id': filename , 'project_id': str(project._id)})
    

@data_router.post("/process_file/{project_id}")
async def process_file(req: Request, project_id: str, data: processData):
    file_id = data.file_id
    chunk_size = data.chunk_size
    overlap = data.overlap
    reset = data.reset

    project_model = await ProjectModel.create_instance(
        db_conn=req.app.state.mongodb_database
    )

    project = await project_model.get_project_or_create(project_id=project_id)

    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(project_id=project_id, filename=file_id)
    chunks = process_controller.process_file_content(file_content=file_content, file_id=file_id,
                                                        chunk_size=chunk_size, chunk_overlap=overlap)
    
    if chunks is None or len(chunks) == 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"signal": models.ResponseStatus.File_processing_failed.value})
    
    chunks_record = [
        DataChunk(chunk_text=chunk.page_content, chunk_metadata=chunk.metadata, chunk_order=i+1, chunk_project_id=project.id)
        for i,chunk in enumerate(chunks)
    ]

    chunk_model = await ChunkModel.create_instance(
        db_conn=req.app.state.mongodb_database
    )

    if reset == 1:
        no_deleted = await chunk_model.delete_chunks_by_project_id(project_id=project.id)

        return JSONResponse(status_code=status.HTTP_200_OK, content={"signal": models.ResponseStatus.File_Processed_Success.value, "deleted_records": no_deleted})

    no_records = await chunk_model.create_chunks_bulk(chunks=chunks_record)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"signal": models.ResponseStatus.File_Processed_Success.value, "inserted_records": no_records})