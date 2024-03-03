from .profile_response import FetchResponse
from ...route_model import ControllerResponse
from .profile_payload import FetchPayload
from ....model.profile_model import ProfileModel
from ....helper.cryptography.jwt import JWT_data 
from typing import Any, Optional
from fastapi import Request
from ....helper.print.colorlog import ColorLog
from ....helper.doc.doc_helper import FetchedData
# from ....database.mongodb.collection import Collections
# from ....repository.profile_repo import profileRepo

async def fetch_handler(req:Request,jwtData:Optional[JWT_data], validated_payload:FetchPayload, fetched_data:FetchedData, params:Any) -> ControllerResponse:
    try:
        _,profiles,err = fetched_data.filter(key="_id",value=validated_payload.profileID,ParsingModel=ProfileModel)
        if err : raise err
        return ControllerResponse(res=FetchResponse(profile=profiles[0]))
    except Exception as error:
        ColorLog.Red(f"fetch_handler error {str(error)}")
        return ControllerResponse(err=error,status_code=500)