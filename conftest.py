from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture
from pytest_asyncio import fixture as async_fixture
from main import app
from src.helper.print.colorlog import ColorLog
from src.helper.cryptography.password import base64String
from httpx import AsyncClient, Response as AsyncResponse


@fixture(scope="session")
def App()->FastAPI:
    return app

@fixture(scope="session")
def Client(App) -> TestClient:
    return TestClient(App)

@async_fixture(scope="session")
async def Async_Client(App):
    async with AsyncClient(app=App, base_url="http://localhost:8000") as asyncClient:
        yield asyncClient
    
@async_fixture(scope="session")
async def Free_Membership_Token(Async_Client:AsyncClient):
    try:
        payload:dict = {
            "email":"chinyan@lifelinelab.io",
            "password":base64String("P@ssw0rd")
        }
        response:AsyncResponse = await Async_Client.post("/v1.0/auth/login",json=payload)
    

        res:dict = response.json()
        
        # assert res.get("data").get("profile").get("name") == "Chin Yan"
        # assert len(res.get("data").get("access_token")) > 0
        return res.get("data").get("access_token")
 
    except Exception as error:
        ColorLog.Red(str(error))
        raise



# from src.helper.cryptography.password import base64String

# @fixture(scope="session")
# def UserToken(Client)->str:
#     payload = {
#         "username": "sleeper_cy_@hotmail.co.uk",
#         "hashedPassword": base64String("Password@123!")
#     }
#     response = Client.post("http://localhost:8888/login",json=payload)
#     assert response.status_code == 200
#     res = response.json()
#     data = res["data"]
#     return data["accessToken"]