# from fastapi import APIRouter
from .public_controller import health_check_handler
from ..route_model import RouteMatrix,HTTP_METHOD
from typing import List

# public_router = APIRouter(prefix="", tags=["public"])
# public_router.add_api_route("/",health_check_handler,methods=["GET"])

public_route_matrices:List[RouteMatrix] = [
    RouteMatrix(
        path="/",
        method=HTTP_METHOD.GET,
        allowed_roles=["*"],
        controller=health_check_handler
    )
]