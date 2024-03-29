# from typing import Coroutine
from .public_response import HealthCheckResponse
from .public_payload import EchoPayload
from ..route_model import ControllerResponse
from ...helper.cryptography.jwt import JWT_data
from ...helper.doc.doc_helper import FetchedData
from typing import Any, Optional,List,Dict
from fastapi import Request

async def health_check_handler(req:Request,jwtData:Optional[JWT_data], validated_payload:None, fetched_data:FetchedData, params:Any)->ControllerResponse:
    try:
        return ControllerResponse(res=HealthCheckResponse(message = "api up and running"))
    except Exception as error:

        return ControllerResponse(err=error,status_code=500)
    
async def echo_handler(req:Request,jwtData:Optional[JWT_data], validated_payload:EchoPayload, fetched_data:FetchedData, params:Any)->ControllerResponse:
    try:
        return ControllerResponse(res=HealthCheckResponse(message = f"You were sending {validated_payload.message}"))
    except Exception as error:
        return ControllerResponse(err=error,status_code=500)