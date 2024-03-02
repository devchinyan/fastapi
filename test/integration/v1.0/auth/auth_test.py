from fastapi.testclient import TestClient
from requests import Response
from httpx import AsyncClient, Response as AsyncResponse
from src.helper.print.colorlog import ColorLog
from src.helper.cryptography.password import base64String
from src.repository.account_repo import accountRepo
from src.repository.profile_repo import profileRepo
import pytest


def test_auth_is_running(Client:TestClient):
    response:Response = Client.get("/v1.0/auth/")
    assert response.status_code == 200
    
    res = response.json()
    print(res)
    ColorLog.Yellow(res)

    assert res == {
        "success": True,
        "error":False,
        "status_code":200,
        'error_object': None,
        "data":{"message": "testing"}
    }

@pytest.mark.asyncio
async def test_login(Async_Client:AsyncClient):
    try:
        payload:dict = {
            "email":"chinyan@lifelinelab.io",
            "password":base64String("P@ssw0rd")
        }
        response:AsyncResponse = await Async_Client.post("/v1.0/auth/login",json=payload)
        assert response.status_code == 200

        res:dict = response.json()
        print(res)
        ColorLog.Yellow(res)
        assert res.get("data").get("profile").get("name") == "Chin Yan"
        assert len(res.get("data").get("access_token")) > 0
 
    except Exception as error:
        ColorLog.Red(str(error))
        raise
            
@pytest.mark.asyncio
async def test_register(Async_Client:AsyncClient):
    try:
        payload:dict = {
            "name":"CheesyChickenBurger",
            "email":"ccb@merrybrown.my",
            "password":base64String("CCB")
        }
        response:AsyncResponse = await Async_Client.post("/v1.0/auth/registration/create", json=payload)
        res:dict = response.json()
        print(res)
        ColorLog.Yellow(res)
        assert res.get("success") == True
        email = payload.get("email")
        await accountRepo.delete("email",email)
        await profileRepo.delete("email",email)
     
    except Exception as error:
        ColorLog.Red(str(error))
        raise