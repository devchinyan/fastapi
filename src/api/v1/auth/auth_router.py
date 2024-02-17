from ...route_model import RouteMatrix
from typing import List
from .auth_controller import test_handler

auth_route_matrices:List[RouteMatrix] = [
    RouteMatrix(
        path="/",
        method="GET",
        allowed_roles=["*"],
        controller=test_handler
    )
]