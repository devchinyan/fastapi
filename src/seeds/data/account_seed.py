from ..seed_model import SeedMatrix
from ...database.mongodb.collection import Collections

accountSeed = SeedMatrix(
    collection_name = Collections.ACCOUNTS,
    data = [
        {
            "_id":"accounts/6f7afd70-21bf-4de5-b60a-16bf8f4fd651",
            "_key":"6f7afd70-21bf-4de5-b60a-16bf8f4fd651",
            "created_at":"2024-03-02T17:46:03.668080",
            "created_by":"profiles/a5253ebb-9a45-465b-b597-497c3b12cf16",
            "updated_at":"2024-03-02T17:46:03.668080",
            "updated_by":"profiles/a5253ebb-9a45-465b-b597-497c3b12cf16",
            "password":{
                "hash":"$2b$12$Mk3LbXmhpAV4YbsyMDM3D.hWPWWO6n3a3v94HZS/Ff2eXyOkg.jIu",
                "salt":"ODc4NjQ="
            },
            "email":"chinyan@lifelinelab.io",
            "profileID":"profiles/a5253ebb-9a45-465b-b597-497c3b12cf16"
        }
    ]
)
