from pydantic import BaseModel

class RegistrationPayload(BaseModel):
    name:str
    email:str
    password:str

class LoginPayload(BaseModel):
    email:str
    password:str