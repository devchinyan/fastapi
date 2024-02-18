from pydantic import BaseModel , Field
from enum import Enum
from typing import Any, List, Callable, Optional, Union
  
class HTTP_METHOD(str, Enum):
    GET="GET"
    PUT="PUT"
    POST="POST"
    DELETE="DELETE"

class Params(BaseModel):
    add_base_field: Optional[List[str]] = None
    escape_uuid_checker: Optional[List[str]] = None

class ControllerResponse(BaseModel):
    res: Optional[Any] = Field(default=None)
    status_code: int = Field(default=200)
    err: Optional[Any] = Field(default=None)

class RouteMatrix(BaseModel):
    path: str
    method: HTTP_METHOD
    allowed_roles: List[str]
    controller: Callable[..., ControllerResponse ]
    params: Optional[Params] = None

class RouteMatrices(BaseModel):
    """
        tag : swagger group title
        group : prefix(path grouping identifier)
    """
    group:str
    tag:str 
    route_matrices:List[RouteMatrix]