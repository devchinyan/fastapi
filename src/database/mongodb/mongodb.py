from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Any
from pydantic import BaseModel
from .collection import Collections
from ...helper.print.colorlog import ColorLog

class Connection(BaseModel):
    res: Any
    err: Any

class MongoDB:
    def __init__(self,username:str,password:str,dbname:str):
        self.uri = f"mongodb+srv://{username}:{password}@fastapimongodb.pkafjzo.mongodb.net/{dbname}?retryWrites=true&w=majority"
        self.username = username
        self.password = password
        self.dbname = dbname
        self.client = None

    def connect(self)-> Connection:
        try:
            if self.client is None :
                self.client = AsyncIOMotorClient(self.uri,username=self.username, password=self.password,)
                ColorLog.Green("mongodb connection created successfully")
                return Connection(res=self.client, err=None) 
            else:
                return Connection(res=self.client, err=None)
       
        except Exception as error:
            return Connection(res=None, err=error)
        
    def get_db(self,dbname = None)->AsyncIOMotorDatabase:
        database_name = self.dbname if dbname is None else dbname
        create_connection = self.connect()
        client = create_connection.res
        db = client[database_name]
        return db
    
    async def setup_collection(self):
        try:
            db = self.get_db()
            collection_names = await db.list_collection_names()
            for col in Collections:
                if(col not in collection_names):
                    await db.create_collection(col)
                    ColorLog.Green(f"created collection : {col}")
                else:
                    ColorLog.Yellow(f"collection exist : {col}")
        except Exception as error:
            ColorLog.Red(error)

        
mongodb = MongoDB(
    username="developer",
    password="developer",
    dbname="app_db"
)

mongodb_client = mongodb.connect()