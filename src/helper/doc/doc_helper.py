from uuid import uuid4
from datetime import datetime
from typing import Optional
from typing import List,Union
from pydantic import BaseModel


def addBaseFields(collection_name:str,doc:Union[BaseModel,dict],profileID:Optional[str]=None)->dict:
    doc = doc if isinstance(doc,dict) else doc.model_dump(by_alias=True)
    key = str(uuid4())
    id = f"{collection_name}/{key}"
    timestamp = datetime.now().isoformat()
    if profileID is None: profileID = id
    added_base_field_doc = {
        "_id":id,
        "_key":key,
        "created_at": timestamp,
        "created_by": profileID,
        "updated_at": timestamp,
        "updated_by": profileID,
         **doc
    }

    return added_base_field_doc 

class FetchedData:
    def __init__(this,fetched:List[dict]):
        this.data:List[dict] = fetched

    def filter(this,key:str,value:str,ParsingModel:BaseModel=None):
        try:
            found = [doc for doc in this.data if doc.get(key) == value]
            if len(found) == 0 : return [],[],None
            parsedData = [ParsingModel(**doc) for doc in found] if ParsingModel is not None else None
            return found,parsedData,None

        except Exception as error:
            return None,None,error
