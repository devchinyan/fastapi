from fastapi import FastAPI, APIRouter
from .v1.v1_router import v1_route_matrices
from .public.public_router import public_route_matrices

def main_router(app:FastAPI):
    public_router = APIRouter(prefix="", tags=["public"])
    for r in public_route_matrices:
        public_router.add_api_route(
            path="/",
            endpoint=r.controller,
            methods=[r.method]
        )

    app.include_router(router=public_router,prefix="")

    for r1 in  v1_route_matrices:
        router = APIRouter(prefix=f"/{r1.group}",tags=[r1.tag])
        for route in r1.route_matrix:

            def controller():
                # middlewares
                
                res = route.controller()
                return res
            

            router.add_api_route(
                path=route.path,
                endpoint=controller,
                methods=[route.method]
            )
            app.include_router(router=router,prefix=f"/v1.0")