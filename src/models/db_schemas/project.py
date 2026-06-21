from pydantic import BaseModel, Field , field_validator
from typing import Optional
from bson.objectid import ObjectId

class project(BaseModel):
    _id: Optional[ObjectId]
    project_id : str = Field(..., min_Length =1)

    @field_validator('project_id')
    @classmethod
    def project_id_must_be_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('project_id must be alphanumeric')
        return v
    
    class Config:
        arbitrary_types_allowed = True

        
