from datetime import datetime, timedelta
from jose import jwt
from src.helper.print.colorlog import ColorLog
from src.config.config import config
from fastapi import Request
from src.model.profile_model import ProfileModel
from .password import pwd_context



class JWT_data(ProfileModel):
    accountID:str
    web_fingerprint:str
    user_role:str
    exp:datetime


def getFingerPrint(req:Request):
    try:
        user_agent = req.headers.get("User-Agent", "None")
        x_forwarded_for = req.headers.get("X-Forwarded-For", req.client.host)
        accept_language = req.headers.get("Accept-Language", "None") 

        web_fingerprint = pwd_context.hash(f"{user_agent}{x_forwarded_for}{accept_language}")
        # web_fingerprint = f"{user_agent}{x_forwarded_for}{accept_language}"
    
        return user_agent,x_forwarded_for,accept_language,web_fingerprint,None
    except Exception as error:
        ColorLog.Red(f"getFingerPrint error : {str(error)}")
        return None,None,None,None,error
    
def verifyFingerPrint(fingerprint1:str,hashed_fingerprint:str)->bool:
    return pwd_context.verify(fingerprint1,hashed_fingerprint)

def generateJWT(data: dict, expires_delta: timedelta = None)->str:
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(config.JWT_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt

def generateJWTRefreshToken(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(config.JWT_REFRESH_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt

def getJwtDATA(token:str):
    try:
        JwtData = jwt.decode(token, config.JWT_SECRET, algorithms=config.JWT_ALGORITHM)
        parsedJWTData = JWT_data(**JwtData)
        return [parsedJWTData,None]
    except Exception as error:
        ColorLog.Red({"error" : error})
        return [None,error]