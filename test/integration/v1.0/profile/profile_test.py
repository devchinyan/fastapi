import pytest
from src.helper.print.colorlog import ColorLog
from httpx import AsyncClient, Response as AsyncResponse

@pytest.mark.asyncio
async def test_fetch_profile(Async_Client:AsyncClient,Free_Membership_Token):
    # try:
        profileID = "profiles/a5253ebb-9a45-465b-b597-497c3b12cf16"
        ColorLog.Yellow("__profileID__ : ",profileID)
        ColorLog.Yellow("__Free_Membership_Token__ : ",Free_Membership_Token)
        response:AsyncResponse = await Async_Client.get(
            url=f"/v1.0/profile/fetch?profileID={profileID}",
            headers={
                "Content-Type":"application/json",
                "Accept": "application/json",
                "Authorization":f"Bearer {Free_Membership_Token}"
            })
        ColorLog.Yellow("__response.text__ : ",response.text)
        res:dict = response.json()
        ColorLog.Yellow("__res__ : ",res)
        assert res.get("success") == True
    # except Exception as error:
    #     ColorLog.Red(f"test_fetch_profile error : {str(error)}")
    #     raise error