from fastapi import FastAPI, APIRouter, Request, Query, Depends
from pydantic import BaseModel as PydanticModel, Field
from typing import Optional
from .v1.v1_router import v1_route_matrices
from .route_model import RouteMatrix, ControllerResponse, HTTP_METHOD
from .public.public_router import public_route_matrices
from ..helper.validator.validator import validation_middleware
from ..helper.print.colorlog import ColorLog
from ..helper.doc.doc_helper import addBaseFields
from ..helper.cryptography.jwt import JWT_data

async def endpoint_func(req:Request,route_matrix:RouteMatrix,validated_payload:Optional[PydanticModel]=None):
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
            grants=route_matrix.grants,
            validated_payload=validated_payload
        )
        if err is not None:
            ColorLog.Magenta("Err 400 or 401 : ",err)
            return Response(success=False,error=True,status_code=400,error_object=str(err),data=None)
        
        if route_matrix.controller.add_base_field_collection is not None:
            jwtData:JWT_data = jwtData
            collection_name = route_matrix.controller.add_base_field_collection
            profile_id = jwtData.id
            added_based_field = addBaseFields(collection_name,validated_payload,profile_id)
            validated_payload = route_matrix.payloadModel(**added_based_field)

        controller_response:ControllerResponse = await route_matrix.controller.func(
            req,
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
    for public_route_matrix in public_route_matrices:
        if public_route_matrix.payloadModel is not None:
            async def respondHandler(
                    req:Request,
                    payload:public_route_matrix.payloadModel = Depends() if public_route_matrix.method == HTTP_METHOD.GET else None,
                    r=Query(default=public_route_matrix,include_in_schema=False)
                ): # type: ignore
                return await endpoint_func(req,public_route_matrix,payload)
        else:
             async def respondHandler(req:Request,public_route_matrix=Query(default=public_route_matrix,include_in_schema=False)):
                return await endpoint_func(req,public_route_matrix)

        public_router.add_api_route(
            path=public_route_matrix.path,
            endpoint=respondHandler,
            methods=[public_route_matrix.method],
            # dependencies=r.payloadModel.schema() if r.payloadModel is not None else None
        )
        

    app.include_router(router=public_router,prefix="")

    for v1_group_route_matrices in  v1_route_matrices:
        router = APIRouter(prefix=f"/{v1_group_route_matrices.group}",tags=[v1_group_route_matrices.tag])
        for v1_group_route_matrix in v1_group_route_matrices.route_matrices:
            if v1_group_route_matrix.payloadModel is not None:
                async def respondHandler(
                        req:Request,
                        payload:v1_group_route_matrix.payloadModel = Depends() if v1_group_route_matrix.method== HTTP_METHOD.GET else None,
                        r=Query(default=v1_group_route_matrix,include_in_schema=False)
                    ): 
                    res = await endpoint_func(req,r,payload)
                    return res
            else:
                async def respondHandler(req:Request,r=Query(default=v1_group_route_matrix,include_in_schema=False)):
                    res = await endpoint_func(req,r)
                    return res

            router.add_api_route(
                path=v1_group_route_matrix.path,
                endpoint=respondHandler,
                methods=[v1_group_route_matrix.method],
            )

            app.include_router(router=router,prefix=f"/v1.0")