from ...route_model import RouteMatrix,HTTP_METHOD, ControllerMatrix
from typing import List
from .auth_controller import test_handler, registration_handler
from .auth_payload import RegistrationPayload
from .auth_response import TestResponse, RegisterResponse

auth_route_matrices:List[RouteMatrix] = [
    RouteMatrix(
        path="/",
        method=HTTP_METHOD.GET,
        grants=["*"],
        controller=ControllerMatrix(func=test_handler),
        responseModel=TestResponse
    ),
    RouteMatrix(
        path="/registration",
        method=HTTP_METHOD.POST,
        grants=["*"],
        controller=ControllerMatrix(func=registration_handler),
        payloadModel=RegistrationPayload,
        responseModel=RegisterResponse
    ),
]