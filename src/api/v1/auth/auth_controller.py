from .auth_response import TestResponse, RegisterResponse
from ...route_model import ControllerResponse
from .auth_payload import RegistrationPayload
from ....helper.cryptography.password import hash
from ....model.profile_model import ProfileFields, ProfileModel
from ....model.account_model import AccountFields, PasswordFields, AccountModel
from ....helper.doc.doc_helper import addBaseFields

async def test_handler() -> ControllerResponse:
    try:
        return ControllerResponse(res=TestResponse(message="testing"))
    except Exception as error:
        return ControllerResponse(err=error,status_code=500)
    
async def registration_handler(payload:RegistrationPayload) -> ControllerResponse:
    try:
        hashResult = hash(password=payload.password)
        profile = addBaseFields(ProfileFields(name=payload.name,emsil = payload.email))
        account = addBaseFields(AccountFields(
            profileID=profile.get("_id"),
            email=payload.email,
            password=PasswordFields(**hashResult.dict()) 
        ))

        return ControllerResponse(res=RegisterResponse(
            message="testing",
            profile=ProfileModel(**profile),
            account=AccountModel(**account)
        ))
    except Exception as error:
        return ControllerResponse(err=error,status_code=500)