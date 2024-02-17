from .mongodb.mongodb import mongodb
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Type
from asyncio import run

mongodb_client:Type[AsyncIOMotorClient] = None

def make_databases_connection():
    try:
        conn = mongodb.connect()
        res = conn.get("res")
        if(res is None): print(conn.get("err"))
        if(res is not None): 
            print("mongodb connected")
            global mongodb_client
            mongodb_client = res
            # insert working
            # db = mongodb_client["app_db"]
            # acc = db["accounts"]
            # acc.insert_one({
            #     "message":"hello world"
            # })
            print(mongodb_client)
    except Exception as error:
        print("connection error : ",error)

def disconnect_databases():
    if mongodb_client is not None:
        mongodb_client.close()
        print("mongo db shuted down")
