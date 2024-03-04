from fastapi import Request
from pydantic import BaseModel
from typing import Type, List, Optional
from re import search, split
from json import loads
from ...helper.cryptography.jwt import getJwtDATA, JWT_data, getFingerPrint, verifyFingerPrint
from ...database.mongodb.base_repository import BaseRepository
from ...api.route_model import HTTP_METHOD
from ...helper.print.colorlog import ColorLog
from ...helper.doc.doc_helper import FetchedData


async def payload_deserialization(req:Request):
    """deserialize payload from request object"""
    try:
        request_method = req.method
        if request_method == HTTP_METHOD.GET:
            payload:dict = req.query_params
        else:
            body_buffer = await req.body()
            serialized_body:str = body_buffer.decode(encoding="utf-8")
            payload:dict = loads(serialized_body)
        return payload, None
    except Exception as err:
        ColorLog.Red("payload_deserialization Err : ",err)
        return None,err

def jwt_validator(req:Request):
    """validate jwt check for format, signature and expired"""
    try:
        headers = req.headers
        Authorization = headers.get("Authorization")
        if(Authorization is None): return  None,Exception("token is required")

        bearer_pattern = r"Bearer "
        if(search(bearer_pattern,Authorization) is None): return None,Exception("token mal-form")
        token = split(bearer_pattern,Authorization)[1].strip()

        jwtData,getJWTErr = getJwtDATA(token)
        if getJWTErr is not None : return None,Exception("token mal-form") 

        user_agent,x_forwarded_for,accept_language,_,getFingerPrintErr = getFingerPrint(req)
        if getFingerPrintErr is not None : return None,Exception("Get Finger Print Error") 

        jwtData:JWT_data = jwtData
        
        web_fingerprint = f"{user_agent}{x_forwarded_for}{accept_language}"
        valid_fingerprint = verifyFingerPrint(web_fingerprint,jwtData.web_fingerprint)
        if not valid_fingerprint: return None,Exception("invalid Finger Print") 

        return jwtData, None

    except Exception as err:
        ColorLog.Red("jwt_validator Err : ",err)
        return None, Exception(f"An error occurred: {err}")
    
def role_validation(jwtData:JWT_data,grants:List[str]):
    """validate user role from jwt with endpoint grants"""
    try:
        role = jwtData.user_role
        if(role in grants or "*" in grants):
            return True,None
        else:
            return False,None
    except Exception as err:
        ColorLog.Red("role_validation Err : ",err)
        return False, err

def payload_validator(payload:dict,payload_model:Type[BaseModel]):
    """validate payload with pydantic model"""
    try:
        validated_payload = None
        if len(list(payload.keys())) > 0 :
            validated_payload = payload_model(**payload)
        return validated_payload,None 
    except Exception as err:
        ColorLog.Red("payload_validator Err : ",err)
        return None,err
    
def get_id_from_payload(payload:dict,exclude:List[str]):
    """Extract all the IDs from db to be validate later"""
    try:
        id_list =[]
        id_pattern = r"(id|Id|ID|ids|IDs)"
        uuid4_pattern =  r'^.*[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'

        keys:list[str] = list(payload.keys())
        if len(keys)==0: return id_list,None
        for key in keys:
            if key in exclude: continue
            # check for key contain id pattern
            if(search(id_pattern,key)):
                if(type(payload[key]).__name__ == "str") : id_list = [*id_list, payload[key]]
                if(type(payload[key]).__name__ == "list"): id_list = [*id_list,*payload[key]]
            #check for value contain uuid4 pattern
            else:
                if(type(payload[key]).__name__ == "str"):
                    if(search(uuid4_pattern,payload[key])): [*id_list, payload[key]]
                if(type(payload[key]).__name__ == "list"):
                    for data in payload[key]:
                        if(type(data).__name__ == "str"):
                            if(search(uuid4_pattern,data)): [*id_list, data]

            #check for nested dict
            if(type(payload[key]).__name__ == "dict"):
                res,err = get_id_from_payload(payload[key],exclude)
                if(err is not None):
                    raise err
                else:
                    id_list = [*id_list,*res]

        return id_list,None

    except Exception as err:
        ColorLog.Red("get_id_from_payload Err : ",err)
        return None,err
    
async def id_validator(ids:List[str]):
    """Validate IDs with db, we only allowed existing id to enter the system"""
    try:
        fetched = []
        if(ids is None): return fetched,None
        if(len(ids)==0): return fetched,None
        for id in ids:
            pattern = r"/"
            collection_name = split(pattern,id)[0]

            collection = BaseRepository(collection_name)

            fetch_response = await collection.fetch(id)
            fetched = [*fetched,fetch_response]
            fetched_data = FetchedData(fetched)
        return fetched_data,None
    except Exception as err:
        ColorLog.Red("id_validator Err : ",err)
        return None,err
    
async def validation_middleware(req:Request,payload_model:Type[BaseModel],exclude_regex:List[str],grants:List[str],validated_payload:Optional[BaseModel]=None):
    """main validation middleware"""
    try:
        jwtData, fetched_data = None, FetchedData([])
        if "*" not in grants:
            jwtData,err = jwt_validator(req)
            if err is not None: return None,None,None,err

        if validated_payload is not None:
            payload,err = await payload_deserialization(req)
            if err is not None: return None,None,None, err

            if payload_model is not None:
                validated_payload,err = payload_validator(payload,payload_model) 
                if err is not None: return None,None,None, err

        if "*" not in grants:
            valid_role,err = role_validation(jwtData,grants)
            if err is not None: return None,None,None,err
            if not valid_role: return None,None,None, Exception("Invalid Role")

        payload = {} if validated_payload is None else validated_payload.model_dump()
        ids,err = get_id_from_payload(payload,exclude_regex)
        if err is not None: return None,None,None, err

        fetched_data,err = await id_validator(ids)
        if err is not None: return None,None,None, err

        return jwtData, validated_payload, fetched_data, None
    except Exception as err:
        ColorLog.Red("validation_middleware Err : ",err)
        return None,None,None, err
