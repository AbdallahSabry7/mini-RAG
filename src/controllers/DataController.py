from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseStatus
import re
import os

class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def is_valid_file(self, file : UploadFile):
        if file.content_type not in self.settings.FILE_TYPE:
            return False, ResponseStatus.File_Type_Not_Supported.value
        
        if file.size > self.settings.FILE_SIZE_LIMIT:
            return False, ResponseStatus.File_Size_Exceeded.value
        
        return True, ResponseStatus.File_Validation_Success.value
    
    def generate_unique_filename(self, original_filename:str , project_id:str):
        random_string = self.generate_random_string(length=10)
        clean_filename = self.clean_filename(original_filename)
        return f"{random_string}_{clean_filename}"


    def clean_filename(self, filename: str):
        filename = filename.replace(" ", "_").lower()
        filename = re.sub(r'[*?<>|":]', '', filename)
        return filename