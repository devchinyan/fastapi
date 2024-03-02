from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture, hookimpl
from main import app
from src.database.mongodb.mongodb import mongodb_client
from motor.core import AgnosticClient
from typing import Type

mongodb_client:AgnosticClient = None

@fixture(scope="session")
def App():
    # db = mongodb_client.get_database()
    # db.
    yield app
    if mongodb_client is not None:
        mongodb_client.close()


@fixture(scope="session")
def Client(App) -> TestClient:
    return TestClient(App)
    



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