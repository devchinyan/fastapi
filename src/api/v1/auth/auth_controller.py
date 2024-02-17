from .auth_response import TestResponse

async def test_handler() -> TestResponse:
    return TestResponse(message="testing")