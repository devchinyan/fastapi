# from fastapi import APIRouter
from .public_controller import health_check_handler, echo_handler
from .public_response import HealthCheckResponse
from .public_payload import EchoPayload
from ..route_model import RouteMatrix, HTTP_METHOD, ControllerMatrix
from typing import List

# public_router = APIRouter(prefix="", tags=["public"])
# public_router.add_api_route("/",health_check_handler,methods=["GET"])

public_route_matrices:List[RouteMatrix] = [
     RouteMatrix(
        path="/",
        method=HTTP_METHOD.GET,
        grants=["*"],
        controller=ControllerMatrix(func=health_check_handler),
        responseModel=HealthCheckResponse
    ),
        RouteMatrix(
        path="/echo",
        method=HTTP_METHOD.POST,
        grants=["*"],
        controller=ControllerMatrix(func=echo_handler),
        payloadModel=EchoPayload,
        responseModel=HealthCheckResponse
    ),
   
]