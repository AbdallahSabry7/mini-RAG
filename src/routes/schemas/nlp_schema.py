from pydantic import BaseModel, Field
from typing import Optional, List

class NLPRequest(BaseModel):
    do_reset : int = 0