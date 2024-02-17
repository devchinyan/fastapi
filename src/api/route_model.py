from pydantic import BaseModel 
from typing import Literal, List, Callable, Optional
  
class Params(BaseModel):
    add_base_field: Optional[List[str]] = None
    escape_uuid_checker: Optional[List[str]] = None

class RouteMatrix(BaseModel):
    path: str
    method: Literal["GET","POST","PUT","DELETE"]
    allowed_roles: List[str]
    controller: Callable
    params: Optional[Params] = None

class RouteMatrices(BaseModel):
    """
        tag : swagger group title
        group : prefix(path grouping identifier)
    """
    group:str
    tag:str 
    route_matrix:List[RouteMatrix]