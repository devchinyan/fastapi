from dotenv import dotenv_values
from pydantic_settings import BaseSettings
from os import environ

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
    
def process_env(filepath:str)->Config:
    env_var = dotenv_values(filepath) 
    keys = list(Config.__annotations__.keys())
    for key in keys:
        env_var[key] = env_var.get(key) if env_var.get(key) is not None else environ.get(key)

    return Config(**env_var) 

config = process_env("env/.env")