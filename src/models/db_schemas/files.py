from pydantic import BaseModel, ConfigDict , Field
from bson.objectid import ObjectId
from datetime import datetime

class FileSchema(BaseModel):
    model_config = ConfigDict(
    arbitrary_types_allowed=True
    )
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    file_name: str = Field(..., min_length=1)
    file_project_id : ObjectId = Field(..., alias="file_project_id")
    file_type: str = Field(..., min_length=1)
    file_size: int = Field(..., ge=0)
    file_config : dict = Field(default={})
    file_push_time : datetime = Field(default=datetime.utcnow)



    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [
                    ('file_project_id', 1),
                ],
                "name": "file_project_id_index",
                "unique": False
            },
            {
                "key": [
                    ('file_project_id', 1),
                    ('file_name', 1),
                ],
                "name": "file_project_id_file_name_index",
                "unique": True
            }
        ]