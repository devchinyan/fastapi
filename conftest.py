from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from pytest import fixture
from main import app
from asyncio import get_event_loop

@fixture
def event_loop():
    loop = get_event_loop()
    yield loop
    loop.close()

@fixture(scope="session")
def App() -> FastAPI:
    return app


@fixture(scope="session")
def Client(App) -> TestClient:
    return TestClient(App)



# from asyncio import get_event_loop
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