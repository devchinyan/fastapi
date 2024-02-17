from pydantic import BaseModel
from typing import Any,List,Dict,Union,Type

class IdCheckerResponse(BaseModel):
    res:List[Dict]
    err:Any

def jwt_validator():
    return True

def payload_validator():
    return True

def role_permission():
    return True

def id_checker(payload)->IdCheckerResponse:
    fetched_doc = []
    dict_payload = payload if isinstance(dict_payload[key],dict) else payload.dict()
    for key in dict_payload.keys():
        if(isinstance(dict_payload[key],dict)):
            idCheckerResponse = id_checker(dict_payload[key])
            if idCheckerResponse.err is not None:
                return IdCheckerResponse(res=None,err=idCheckerResponse.err) 
            elif  idCheckerResponse.res is not None:
                fetched_doc = [ *fetched_doc, *idCheckerResponse.res ]
        else:
            # 1. regexp check if key name has id/ids fetch
            # 2. regexp check if uuid fetch
            return IdCheckerResponse(res=fetched_doc,err=None)
