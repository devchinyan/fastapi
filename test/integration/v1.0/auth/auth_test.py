from requests import Request,Response
from src.helper.print.colorlog import ColorLog
# import asyncio

def test_server_is_up_and_running(Client:Request):
    response:Response = Client.get("/v1.0/auth/")
    assert response.status_code == 200

    assert response.json() == {"message": "testing"}