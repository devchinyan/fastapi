from ....model.profile_model import ProfileModel
from pydantic import BaseModel

class FetchResponse(BaseModel):
    profile:ProfileModel