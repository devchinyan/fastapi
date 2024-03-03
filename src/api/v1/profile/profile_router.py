from ...route_model import RouteMatrix,HTTP_METHOD, ControllerMatrix
from typing import List
from .profile_controller import fetch_handler
from .profile_payload import FetchPayload
from .profile_response import FetchResponse
from src.model.profile_model import UserRoleEnum

profile_route_matrices:List[RouteMatrix] = [
    RouteMatrix(
        path="/fetch",
        method=HTTP_METHOD.GET,
        grants=[UserRoleEnum.FREE_MEMBERSHIP],
        controller=ControllerMatrix(func=fetch_handler),
        payloadModel=FetchPayload,
        responseModel=FetchResponse
    ),
]