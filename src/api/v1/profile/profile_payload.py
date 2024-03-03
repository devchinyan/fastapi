from pydantic import BaseModel

class FetchPayload(BaseModel):
    profileID:str