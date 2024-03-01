from uuid import uuid4
from datetime import datetime
from typing import Optional

def addBaseFields(collection_name:str,doc,profileID:Optional[str]=None)->dict:
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
