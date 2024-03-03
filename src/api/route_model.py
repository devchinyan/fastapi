from pydantic import BaseModel , Field
from enum import Enum
from typing import Any, List, Callable, Optional
from fastapi import Request
from ..helper.doc.doc_helper import FetchedData
from ..helper.cryptography.jwt import JWT_data


class HTTP_METHOD(str, Enum):
    GET="GET"
    PUT="PUT"
    POST="POST"
    DELETE="DELETE"

class ControllerResponse(BaseModel):
    res: Optional[Any] = Field(default=None)
    status_code: int = Field(default=200)
    err: Optional[Any] = Field(default=None)

# def Controller(req:Request,jwtData:Optional[JWT_data], validated_payload:FetchPayload, fetched_data:FetchedData, params:Any)-> ControllerResponse:
Controller =  Callable[[Request,Optional[JWT_data], Optional[BaseModel], FetchedData, Any], ControllerResponse ]

class ControllerMatrix(BaseModel):
    func: Controller
    params: Optional[Any] = Field(default=None)
    add_base_field_collection: Optional[str] = Field(default=None)
    escape_uuid_checker: Optional[List[str]] = Field(default=[])

class RouteMatrix(BaseModel):
    path: str
    method: HTTP_METHOD
    grants: List[str]
    controller: ControllerMatrix
    payloadModel:Optional[Any] = Field(default=None)
    responseModel:Any

class RouteMatrices(BaseModel):
    """
        tag : swagger group title
        group : prefix(path grouping identifier)
    """
    group:str
    tag:str 
    route_matrices:List[RouteMatrix]