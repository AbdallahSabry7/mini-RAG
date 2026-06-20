from enum import Enum

class ResponseStatus(Enum):
    File_Type_Not_Supported = "File type not supported."
    File_Size_Exceeded = "File size exceeds the limit."
    File_Validation_Success = "File is valid."
    File_Upload_Success = "File uploaded successfully."
    File_Processed_Success = "File processed successfully."
    File_processing_failed = "Failed to process file content."
    File_Upload_Failed = "Failed to upload file."