from pydantic import BaseModel

class EchoPayload(BaseModel):
    message:str