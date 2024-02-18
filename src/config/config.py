from dotenv import dotenv_values
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    MONGODB_USERNAME:str
    MONGODB_PASSWORD:str
    MONGODB_DBNAME:str
    
config = Config(**dotenv_values("env/.env")) 