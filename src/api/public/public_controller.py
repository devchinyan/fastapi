# from typing import Coroutine
from .public_response import HealthCheckResponse
from ..route_model import ControllerResponse

async def health_check_handler()->ControllerResponse:
    try:
        return ControllerResponse(res=HealthCheckResponse(**{"message": "api up and running"}))
    except Exception as error:
        return ControllerResponse(err=error,status_code=500)