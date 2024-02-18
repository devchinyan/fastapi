from .auth_response import TestResponse
from ...route_model import ControllerResponse

async def test_handler() -> ControllerResponse:
    try:
        return ControllerResponse(res=TestResponse(message="testing"))
    except Exception as error:
        return ControllerResponse(err=error,status_code=500)