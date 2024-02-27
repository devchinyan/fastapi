from datetime import datetime, timedelta
from jose import jwt
from src.helper.print.colorlog import ColorLog
from src.config.config import config

def generateJWT(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
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
        return [JwtData,None]
    except Exception as error:
        ColorLog.Red({"error" : error})
        return [None,error]