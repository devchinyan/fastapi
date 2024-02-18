from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture
from main import app
# from src.helper.cryptography.password import base64String


@fixture(scope="session")
def App() -> FastAPI:
    return app


@fixture(scope="session")
def Client(App) -> TestClient:
    return TestClient(App)

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