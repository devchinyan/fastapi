from uuid import uuid4
from datetime import datetime

def addBaseFields(doc,profileID:str,collection_name:str)->dict:
    doc = doc if isinstance(doc,dict) else doc.dict()
    key = uuid4()
    timestamp = datetime.now().isoformat()
    id = f"{collection_name}/{key}"

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
