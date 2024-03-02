from typing import List
from pydantic import BaseModel

class SeedMatrix(BaseModel):
    collection_name:str
    data: List[dict]