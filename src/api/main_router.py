from fastapi import FastAPI, APIRouter,Request
from pydantic import BaseModel as PydanticModel, Field
from typing import Optional
from .v1.v1_router import v1_route_matrices
from .route_model import RouteMatrix, ControllerResponse
from .public.public_router import public_route_matrices
from ..helper.validator.validator import validation_middleware
from ..helper.doc.doc_helper import addBaseFields
from ..helper.print.colorlog import ColorLog

async def endpoint_func(req:Request,route_matrix:RouteMatrix):
    try:
        ColorLog.Magenta("endpoint_func is running")
        class Response(PydanticModel):
            success: bool
            error: bool
            status_code:int
            error_object: Optional[str] = Field(default=None)
            data: Optional[route_matrix.responseModel] = Field(default=None)

        jwtData, validated_payload, fetched_data, err = await validation_middleware(
            req,
            payload_model=route_matrix.payloadModel,
            exclude_regex=route_matrix.controller.escape_uuid_checker,
            grants=route_matrix.grants
        )
        if err is not None:
            return Response(success=False,error=True,status_code=400,error_object=str(err),data=None)
        
        if route_matrix.controller.add_base_field_collection is not None:
            collection_name = route_matrix.controller.add_base_field_collection
            profile_id = jwtData.get("profileID")
            added_based_field = addBaseFields(validated_payload,profile_id,collection_name)
            validated_payload = route_matrix.payloadModel(**added_based_field)

        controller_response:ControllerResponse = await route_matrix.controller.func(
            jwtData, 
            validated_payload, 
            fetched_data, 
            params=route_matrix.controller.params
        )
        if controller_response.err is not None:
            return Response(
                success=False,
                error=True,
                status_code=controller_response.status_code,
                error_object=str(controller_response.err),
                data=None
            )
        
        return Response(
            success=True,
            error=False,
            status_code=200,
            data=controller_response.res
        )
    except Exception as err:
        ColorLog.Red("endpoint_func error : ",err)


def main_router(app:FastAPI):
    public_router = APIRouter(prefix="", tags=["public"])
    for r in public_route_matrices:
       
        async def respondHandler(req:Request,r=r):
            return await endpoint_func(req,r)
        ColorLog.Magenta(f"{r.method} : {r.path}")
        public_router.add_api_route(
            path=r.path,
            endpoint=respondHandler,
            methods=[r.method],
        )

    app.include_router(router=public_router,prefix="")

    for r1 in  v1_route_matrices:
        router = APIRouter(prefix=f"/{r1.group}",tags=[r1.tag])
        for route in r1.route_matrices:
            if route.payloadModel is not None:
                async def respondHandler(req:Request,r=r):
                    return endpoint_func(req,r)

            router.add_api_route(
                path=route.path,
                endpoint=respondHandler,
                methods=[route.method],
            )
            app.include_router(router=router,prefix=f"/v1.0")