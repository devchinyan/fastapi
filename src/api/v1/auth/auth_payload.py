from pydantic import BaseModel

class RegistrationPayload(BaseModel):
    name:str
    email:str
    password:str