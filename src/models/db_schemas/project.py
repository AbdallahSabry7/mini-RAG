from pydantic import BaseModel, ConfigDict, Field , field_validator
from typing import Optional
from bson.objectid import ObjectId

class project(BaseModel):
    model_config = ConfigDict(
    arbitrary_types_allowed=True
    )
        
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    project_id : str = Field(..., min_length =1)

    @field_validator('project_id')
    @classmethod
    def project_id_must_be_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('project_id must be alphanumeric')
        return v
    
    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [
                    ('project_id', 1),
                ],
                "name": "project_id_index",
                "unique": True
            }
        ]
    

        
