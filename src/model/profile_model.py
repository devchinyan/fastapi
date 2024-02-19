from .base_model import BaseModel, uuid_pattern
from pydantic import Field, constr
from ..database.mongodb.collection import Collections

class ProfileModel(BaseModel):
    id:constr(pattern=f"{Collections.PROFILES}/{uuid_pattern}") = Field(alias="_id")