from pydantic import BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel):
    _id:str
    _key:str

    created_by:str
    created_at:str
    updated_by:str
    updated_at:str
