from dotenv import dotenv_values
from pydantic_settings import BaseSetting

class Config(BaseSetting):
    MONGODB_USERNAME:str
    MONGODB_DBNAME:str
    MONGODB_URL:str

config = Config(**dotenv_values("env/test.env")) 