from requests import Request,Response
from src.helper.print.colorlog import ColorLog
# import asyncio

def test_server_is_up_and_running(Client:Request):
    response:Response = Client.get("/")
    assert response.status_code == 200

    res = response.json()
    ColorLog.Yellow(res)
    
    assert res == {
        "success": True,
        "error":False,
        "status_code":200,
        "data":{"message": "api up and running"}
    }