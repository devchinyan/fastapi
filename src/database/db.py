from .mongodb.mongodb import mongodb
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Type
# from asyncio import run
# from uuid import uuid4
from src.helper.print.colorlog import ColorLog
mongodb_client:Type[AsyncIOMotorClient] = None

async def make_databases_connection():
    try:
        conn = mongodb.connect()
        res = conn.res
        if(res is None): ColorLog.Red(conn.err)
        if(res is not None): 
            print("mongodb connected")
            global mongodb_client
            mongodb_client = res
            # insert working
            # db = mongodb_client["app_db"]
            # acc = db["accounts"]
            # key = str(uuid4())
            # id = f"accounts/{key}"
            # acc.insert_one({
            #     "_id":id,
            #     "_key":key,
            #     "message":"hello world"
            # })
            print(mongodb_client)
        await mongodb.setup_collection()
    except Exception as error:
        print("connection error : ",error)

def disconnect_databases():
    if mongodb_client is not None:
        mongodb_client.close()
        print("mongo db shuted down")
