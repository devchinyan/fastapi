from .auth_response import TestResponse, RegisterResponse
from ...route_model import ControllerResponse
from .auth_payload import RegistrationPayload
from ....helper.cryptography.password import hash
from ....model.profile_model import ProfileFields, ProfileModel
from ....model.account_model import AccountFields, PasswordFields, AccountModel
from ....helper.doc.doc_helper import addBaseFields
from typing import Any, Optional,List,Dict

async def test_handler(jwtData:Optional[dict], validated_payload:Any, fetched_data:List[Dict], params:Any) -> ControllerResponse:
    try:
        return ControllerResponse(res=TestResponse(message="testing"))
    except Exception as error:
        return ControllerResponse(err=error,status_code=500)
    
async def registration_handler(jwtData:Optional[dict], validated_payload:RegistrationPayload, fetched_data:List[Dict], params:Any) -> ControllerResponse:
    try:
        hashResult = hash(password=validated_payload.password)
        profile = addBaseFields(ProfileFields(name=validated_payload.name,email = validated_payload.email))
        account = addBaseFields(AccountFields(
            profileID=profile.get("_id"),
            email=validated_payload.email,
            password=PasswordFields(**hashResult.dict()) 
        ))

        return ControllerResponse(res=RegisterResponse(
            message="testing",
            profile=ProfileModel(**profile),
            account=AccountModel(**account)
        ))
    except Exception as error:
        return ControllerResponse(err=error,status_code=500)