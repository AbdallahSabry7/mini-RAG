from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseStatus

class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def is_valid_file(self, file : UploadFile):
        if file.content_type not in self.settings.FILE_TYPE:
            return False, ResponseStatus.File_Type_Not_Supported.value
        
        if file.size > self.settings.FILE_SIZE_LIMIT:
            return False, ResponseStatus.File_Size_Exceeded.value
        
        return True, ResponseStatus.File_Validation_Success.value