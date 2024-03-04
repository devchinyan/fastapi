from dotenv import dotenv_values
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    HOST:str
    PORT:str
    MONGODB_USERNAME:str
    MONGODB_PASSWORD:str
    MONGODB_DBNAME:str
    MONGODB_CONSTR:str
    JWT_SECRET:str
    JWT_ALGORITHM:str
    JWT_EXPIRE_MINUTES:int
    JWT_REFRESH_MINUTES:int
    
config = Config(**dotenv_values("env/.env")) 