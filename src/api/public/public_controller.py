# from typing import Coroutine
from .public_response import HealthCheckResponse
from .public_payload import EchoPayload
from ..route_model import ControllerResponse
from ...helper.print.colorlog import ColorLog
from typing import Any, Optional,List,Dict

async def health_check_handler(jwtData:Optional[dict], validated_payload:None, fetched_data:List[Dict], params:Any)->ControllerResponse:
    try:
        return ControllerResponse(res=HealthCheckResponse(message = "api up and running"))
    except Exception as error:

        return ControllerResponse(err=error,status_code=500)
    
async def echo_handler(jwtData:Optional[dict], validated_payload:EchoPayload, fetched_data:List[Dict], params:Any)->ControllerResponse:
    try:
        return ControllerResponse(res=HealthCheckResponse(message = f"You were sending {validated_payload.message}"))
    except Exception as error:
        return ControllerResponse(err=error,status_code=500)