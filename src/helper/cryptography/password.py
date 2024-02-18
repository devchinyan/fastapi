from pydantic import BaseModel as PydanticBaseModel
from passlib.context import CryptContext
import base64
from random import randint

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

generate_otp = lambda: f"{randint(0,9999)}".rjust(4,"0")

def randomSalt()->str:
    randomNumb = f'{randint(0,99999)}'
    stringBytes = randomNumb.encode("ascii")
    base64_bytes = base64.b64encode(stringBytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def base64String(input:str)->str:
    stringBytes = input.encode("ascii")
    base64_bytes = base64.b64encode(stringBytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

class HashResult(PydanticBaseModel):
    salt:str
    hash:str

def hash(password:str)->HashResult:
    salt:str = randomSalt()
    stringBytes = f"{password}{salt}".encode("ascii")
    base64_bytes = base64.b64encode(stringBytes)
    base64_string = base64_bytes.decode("ascii")
    return HashResult(salt=salt,hash=pwd_context.hash(base64_string))

def verify_password(password:str,salt:str, hashed_password:str)->bool:
    stringBytes = f"{password}{salt}".encode("ascii")
    base64_bytes = base64.b64encode(stringBytes)
    base64_string = base64_bytes.decode("ascii")
    return pwd_context.verify(base64_string, hashed_password)
