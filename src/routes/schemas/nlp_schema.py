from pydantic import BaseModel, Field
from typing import Optional, List

class NLPRequest(BaseModel):
    do_reset : int = 0

class SearchRequest(BaseModel):
    text : str = Field(..., description="The text to search for in the vector database.")
    limit : Optional[int] = Field(10, description="The maximum number of search results to return.")