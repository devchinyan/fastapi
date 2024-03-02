from .mongodb import mongodb
from motor.core import AgnosticCollection
from pydantic import BaseModel
from typing import Optional, Tuple
class BaseRepository:
    def __init__(self,collection_name:str):
        self.collection_name = collection_name
        self.db = mongodb.get_db()
        self.collection:AgnosticCollection = self.db[self.collection_name]

    async def create(self,doc:dict):
         await self.collection.insert_one(document=doc)
         return doc

    async def fetch(self,doc_id:str):
        fetched = await self.collection.find_one(filter={"_id": doc_id})
        return fetched
    
    async def find_one(self,query:dict,Model:Optional[BaseModel]=None)->Tuple[Optional[dict],Optional[BaseModel],Optional[Exception]]:
        try:
            fetched = await self.collection.find_one(filter=query)
            if fetched is None: return None, None, None
            if Model is None:
                return fetched,None,None
            else:
                parsed = Model(**fetched)
                return fetched,parsed,None
        except Exception as error:
            return None,None,error

    async def update(self,doc_id:str,doc_updates:dict):
        updated_doc = await self.collection.find_one_and_update(
            filter={"_id": doc_id},
            update={"$set": doc_updates},
            return_document=True  
        )
        return updated_doc
    
    async def delete(self,field_name:str,field_value):
        query = {field_name:field_value}
        deleted_doc = await self.collection.find_one_and_delete(filter=query)
        return deleted_doc
    