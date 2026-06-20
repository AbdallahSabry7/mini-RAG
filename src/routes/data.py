from fastapi import Depends, FastAPI , APIRouter ,UploadFile , status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, Settings
from controllers import DataController , ProcessController

data_router = APIRouter(
    prefix = "/api/v1/data",
    tags = ['api_v1','data']
)

@data_router.post("/process/{project_id}")
async def process_data(project_id: str, file: UploadFile,
                    settings: Settings = Depends(get_settings)):
    
    is_valid , message = DataController().is_valid_file(file = file)
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": message})
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "File is valid and ready for processing."})
    
    folder_path = ProcessController().get_file_path(project_id = project_id)
    file_location = os.path.join(folder_path, file.filename)
    