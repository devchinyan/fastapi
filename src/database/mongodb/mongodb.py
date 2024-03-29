from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticCollection, AgnosticDatabase
from typing import Any, List
from pydantic import BaseModel
from .collection import Collections
from ...helper.print.colorlog import ColorLog
from src.seeds.seed_model import SeedMatrix
from asyncio import get_running_loop
from src.config.config import config

from pymongo.results import UpdateResult
class Connection(BaseModel):
    res: Any
    err: Any

class MongoDB:
    def __init__(self,username:str,password:str,dbname:str):
        self.uri = config.MONGODB_CONSTR
        self.username = username
        self.password = password
        self.dbname = dbname
        self.client = None

    def connect(self)-> Connection:
        try:
            if self.client is None :
                self.client = AsyncIOMotorClient(self.uri,username=self.username, password=self.password,)
                self.client.get_io_loop = get_running_loop
                ColorLog.Green("mongodb connection created successfully")
                return Connection(res=self.client, err=None) 
            else:
                return Connection(res=self.client, err=None)
       
        except Exception as error:
            return Connection(res=None, err=error)
        
    def get_db(self,dbname = None)->AgnosticDatabase:
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

    async def seed_data(self,seedMatrices:List[SeedMatrix]):
        try:
            db = self.get_db()
            for seedMatrix in seedMatrices:
                col:AgnosticCollection = db[seedMatrix.collection_name]
                upserted = 0
                for doc in seedMatrix.data:
                    if doc.get("_id") is None: continue
                    result:UpdateResult = await col.update_one(
                        filter={"_id":doc["_id"]},
                        update={"$set":doc},
                        upsert=True
                    )
                    upserted += 1 if result.upserted_id is not None else 0
                ColorLog.Green(f"UPSERTED {upserted} data into {seedMatrix.collection_name}")
                    


        except Exception as error:
            ColorLog.Red("seed_data : ",error)

        
mongodb = MongoDB(
    username="developer",
    password="developer",
    dbname="app_db"
)

mongodb_connection = mongodb.connect()
mongodb_client = mongodb_connection.res