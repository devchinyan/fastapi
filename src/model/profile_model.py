from .base_model import BaseModel, uuid_pattern
from pydantic import Field, constr, BaseModel as PydanticModel
from ..database.mongodb.collection import Collections
from enum import Enum

class UserRoleEnum(str, Enum):
    FREE_MEMBERSHIP = 'FREE_MEMBERSHIP'
    PREMIUM_MEMBERSHIP = 'PREMIUM_MEMBERSHIP'
    SUPER_ADMIN = 'SUPER_ADMIN'

profileID = constr(pattern=f"{Collections.PROFILES}/{uuid_pattern}")


class ProfileFields(PydanticModel):
    name:str
    email:str
    user_role: UserRoleEnum
    
class ProfileModel(BaseModel,ProfileFields):
    id:profileID = Field(alias="_id")