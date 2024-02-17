from motor.motor_asyncio import AsyncIOMotorClient,AsyncIOMotorDatabase
from typing import Dict, Union, Optional

class MongoDB:
    def __init__(self,username:str,password:str,dbname:str):
        self.uri = f"mongodb+srv://{username}:{password}@fastapimongodb.pkafjzo.mongodb.net/{dbname}?retryWrites=true&w=majority"
        self.username = username
        self.password = password
        self.dbname = dbname
        self.client = None

    def connect(self)-> Dict[str, Union[Optional[AsyncIOMotorClient], Optional[Exception]]]:
        try:
            if self.client is None :
                 self.client = AsyncIOMotorClient(self.uri,username=self.username, password=self.password,)
                 return {"res":self.client , "err":None}
            else:
                return {"res":self.client , "err":None}
        except Exception as error:
            return {"res":None, "err":error}
        
    def get_db(self,dbname = None)->AsyncIOMotorDatabase:
        database_name = self.dbname if dbname is None else dbname
        create_connection = self.connect()
        client = create_connection.get("res")
        db = client[database_name]
        return db
        
mongodb = MongoDB(
    username="developer",
    password="developer",
    dbname="app_db"
)

mongodb_client = mongodb.connect()