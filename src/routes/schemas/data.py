from pydantic import BaseModel
from typing import Optional


class processData(BaseModel):
    file_id: str
    chunk_size: Optional[int] = 100
    overlap: Optional[int] = 20
    reset: Optional[bool] = False