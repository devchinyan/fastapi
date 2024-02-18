from ...route_model import RouteMatrix,HTTP_METHOD
from typing import List
from .auth_controller import test_handler

auth_route_matrices:List[RouteMatrix] = [
    RouteMatrix(
        path="/",
        method=HTTP_METHOD.GET,
        allowed_roles=["*"],
        controller=test_handler
    )
]