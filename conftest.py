from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture
from pytest_asyncio import fixture as async_fixture
from main import app
from src.database.mongodb.mongodb import mongodb_client
from motor.core import AgnosticClient
from httpx import AsyncClient


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