from ..route_model import RouteMatrices
from typing import List
from .auth.auth_router import auth_route_matrices
from .profile.profile_router import profile_route_matrices

v1_route_matrices:List[RouteMatrices] = [
    RouteMatrices(
        group = "auth",
        tag="auth",
        route_matrices=auth_route_matrices
    ),
    RouteMatrices(
        group = "profile",
        tag="profile",
        route_matrices=profile_route_matrices
    )
]