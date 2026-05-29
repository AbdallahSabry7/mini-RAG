from .BaseController import BaseController
from fastapi import UploadFile

class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def is_valid_file(self, file : UploadFile):
        if file.content_type not in self.settings.FILE_TYPE:
            return False, f"Invalid file type. Allowed types: {', '.join(self.settings.FILE_TYPE)}"
        
        if file.size > self.settings.FILE_SIZE_LIMIT:
            return False, f"File size exceeds the limit of {self.settings.FILE_SIZE_LIMIT} bytes."
        
        return True, "File is valid."