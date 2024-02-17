from ..route_model import RouteMatrices
from typing import List
from .auth.auth_router import auth_route_matrices

v1_route_matrices:List[RouteMatrices] = [
    RouteMatrices(
        group = "auth",
        tag="auth",
        route_matrix=auth_route_matrices
    )
]