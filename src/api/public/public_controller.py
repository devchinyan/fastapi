# from typing import Coroutine
from .public_response import HealthCheckResponse

async def health_check_handler()->HealthCheckResponse:
    return HealthCheckResponse(**{"message": "api up and running"})