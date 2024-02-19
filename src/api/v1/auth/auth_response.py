from pydantic import BaseModel
from ....model.profile_model import ProfileModel
from ....model.account_model import AccountModel

class TestResponse(BaseModel):
    message:str

class RegisterResponse(TestResponse):
    profile:ProfileModel
    account:AccountModel