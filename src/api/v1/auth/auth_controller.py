from .auth_response import TestResponse, RegisterResponse,LoginResponse
from ...route_model import ControllerResponse
from .auth_payload import RegistrationPayload,LoginPayload
from ....helper.cryptography.password import verify_password, hash
from ....helper.cryptography.jwt import getFingerPrint, generateJWT
from ....model.profile_model import ProfileFields, ProfileModel, UserRoleEnum
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
            ProfileFields(name=validated_payload.name,email = validated_payload.email,user_role=UserRoleEnum.FREE_MEMBERSHIP)
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
    

async def login_handler(req:Request,jwtData:Optional[dict], validated_payload:LoginPayload, fetched_data:List[Dict], params:Any) -> ControllerResponse:
    try:
        # validate user
        ColorLog.Cyan(validated_payload)
        account,parsedAccount,err = await accountRepo.find_one({"email":validated_payload.email},AccountModel)
        if err is not None: raise err
        if account is None : return ControllerResponse(err=Exception("Invalid Email or Password 1"),status_code=401)

        profile,_,err = await profileRepo.find_one({"email":validated_payload.email})
        if err is not None: raise err
        if profile is None: return ControllerResponse(err=Exception("Profile Doesn't Exist"),status_code=401)

        parsedAccount:AccountModel = parsedAccount
        password, saltedHash,salt = validated_payload.password, parsedAccount.password.hash, parsedAccount.password.salt
        ColorLog.Cyan(password,salt,saltedHash)
        valid = verify_password(password=password,salt=salt,hashed_password=saltedHash)
        if valid == False : return ControllerResponse(err=Exception("Invalid Email or Password 2"),status_code=401)
        ColorLog.Cyan("valid value = ",valid)
        # log login data
        user_agent,x_forwarded_for,accept_language,web_fingerprint,err = getFingerPrint(req)
        if err : ColorLog.Red("getFingerPrint err : ",err)
        
     
        
        ColorLog.Green(profile)
        # generate jwt
        access_token = generateJWT({
            "accountID":account["_id"],
            "web_fingerprint":web_fingerprint,
            **profile
        })
   
        return ControllerResponse(res=LoginResponse(
            profile=profile,
            access_token = access_token,
            web_fingerprint=web_fingerprint, 
            user_agent=user_agent, 
            x_forwarded_for=x_forwarded_for,
            accept_language=accept_language 
        ))
    
    except Exception as error:
        ColorLog.Red(error)
        return ControllerResponse(err=error,status_code=500)

