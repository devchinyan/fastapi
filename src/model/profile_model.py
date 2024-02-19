from .base_model import BaseModel, uuid_pattern
from pydantic import Field, constr, BaseModel as PydanticModel
from ..database.mongodb.collection import Collections

profileID = constr(pattern=f"{Collections.PROFILES}/{uuid_pattern}")

class ProfileFields(PydanticModel):
    name:str
    email:str
    
class ProfileModel(BaseModel,ProfileFields):
    id:profileID = Field(alias="_id")