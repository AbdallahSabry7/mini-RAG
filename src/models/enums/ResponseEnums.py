from enum import Enum

class ResponseStatus(Enum):
    File_Type_Not_Supported = "File type not supported."
    File_Size_Exceeded = "File size exceeds the limit."
    File_Validation_Success = "File is valid."
    File_Upload_Success = "File uploaded successfully."