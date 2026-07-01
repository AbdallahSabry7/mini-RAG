from pydantic import BaseModel
from typing import Optional


class processData(BaseModel):
    file_id: str = None
    chunk_size: Optional[int] = 100
    overlap: Optional[int] = 20
    reset: Optional[int] = 0