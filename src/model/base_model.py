from pydantic import BaseModel as PydanticBaseModel, constr
from datetime import datetime
from ..database.mongodb.collection import Collections

uuid_pattern = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89aAbB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}"

class BaseModel(PydanticBaseModel):
    _key:constr(pattern=uuid_pattern) 

    created_by:constr(pattern=f"{Collections.PROFILES}/{uuid_pattern}")
    created_at:datetime
    updated_by:constr(pattern=f"{Collections.PROFILES}/{uuid_pattern}")
    updated_at:datetime
