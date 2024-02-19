from .base_model import BaseModel, uuid_pattern
from pydantic import Field, constr
from ..database.mongodb.collection import Collections

class AccountModel(BaseModel):
    id:constr(pattern=f"{Collections.ACCOUNTS}/{uuid_pattern}") = Field(alias="_id")