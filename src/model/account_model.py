from .base_model import BaseModel, uuid_pattern
from pydantic import BaseModel as PydanticModel, Field, constr
from ..database.mongodb.collection import Collections
from .profile_model import profileID

accountID = constr(pattern=f"{Collections.ACCOUNTS}/{uuid_pattern}")
class PasswordFields(PydanticModel):
    hash:str
    salt:str

class AccountFields(PydanticModel):
    password:PasswordFields
    email:str
    profileID: profileID
    
class AccountModel(BaseModel,AccountFields):
    id:accountID = Field(alias="_id")