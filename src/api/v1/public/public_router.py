from fastapi import APIRouter
from .public_controller import health_check_handler

public_router = APIRouter(prefix="", tags=["public"])
public_router.add_api_route("/",health_check_handler,methods=["GET"])