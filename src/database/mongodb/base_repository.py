from .mongodb import mongodb
from motor.motor_asyncio import AsyncIOMotorCollection

class BaseRepository:
    def __init__(self,collection_name:str):
        self.collection_name = collection_name
        self.db = mongodb.get_db()
        self.collection:AsyncIOMotorCollection = self.db[self.collection_name]

    async def create(self,doc:dict):
         await self.collection.insert_one(doc)
         return doc

    async def fetch(self,doc_id:str):
        fetched = await self.collection.find_one({"_id": doc_id})
        return fetched

    async def update(self,doc_id:str,doc_updates:dict):
        updated_doc = await self.collection.find_one_and_update(
            {"_id": doc_id},
            {"$set": doc_updates},
            return_document=True  
        )
        return updated_doc
    