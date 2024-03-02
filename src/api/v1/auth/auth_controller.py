from .auth_response import TestResponse, RegisterResponse
from ...route_model import ControllerResponse
from .auth_payload import RegistrationPayload
from ....helper.cryptography.password import hash
from ....model.profile_model import ProfileFields, ProfileModel
from ....model.account_model import AccountFields, PasswordFields, AccountModel
from ....helper.doc.doc_helper import addBaseFields
from typing import Any, Optional,List,Dict
from fastapi import Request
from ....helper.print.colorlog import ColorLog
from ....database.mongodb.collection import Collections
from ....repository.account_repo import accountRepo
from ....repository.profile_repo import profileRepo

async def test_handler(req:Request,jwtData:Optional[dict], validated_payload:Any, fetched_data:List[Dict], params:Any) -> ControllerResponse:
    try:
        return ControllerResponse(res=TestResponse(message="testing"))
    except Exception as error:
        return ControllerResponse(err=error,status_code=500)
    
async def registration_handler(req:Request,jwtData:Optional[dict], validated_payload:RegistrationPayload, fetched_data:List[Dict], params:Any) -> ControllerResponse:
    try:
        hashResult = hash(password=validated_payload.password)
        profile = addBaseFields(
            Collections.PROFILES,
            ProfileFields(name=validated_payload.name,email = validated_payload.email)
        )
        account = addBaseFields(
            Collections.ACCOUNTS,
            AccountFields(
                profileID=profile.get("_id"),
                email=validated_payload.email,
                password=PasswordFields(**hashResult.model_dump()) 
            ),profile.get("_id")
        )

        created_profile = await profileRepo.create(profile)
        created_account = await accountRepo.create(account)
       


        return ControllerResponse(res=RegisterResponse(
            message="Registration",
            profile=ProfileModel(**created_profile),
            # account =AccountModel(**created_account)
        ))
    except Exception as error:
        return ControllerResponse(err=error,status_code=500)
    

async def login_handler(req:Request,jwtData:Optional[dict], validated_payload:RegistrationPayload, fetched_data:List[Dict], params:Any) -> ControllerResponse:
    try:

        # validate user

        # log login data

        # generate fingerprint and jwt
        return ControllerResponse(res=RegisterResponse(
            message="logined",
        ))
    except Exception as error:
        return ControllerResponse(err=error,status_code=500)

