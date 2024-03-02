from pydantic import BaseModel
from ....model.profile_model import ProfileModel
# from ....model.account_model import AccountModel

class TestResponse(BaseModel):
    message:str

class RegisterResponse(TestResponse):
    profile:ProfileModel
    # account:AccountModel

class LoginResponse(BaseModel):
    profile:ProfileModel
    access_token: str
    web_fingerprint:str 
    user_agent:str
    x_forwarded_for:str
    accept_language:str