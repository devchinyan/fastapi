from ..seed_model import SeedMatrix
from src.database.mongodb.collection import Collections
from src.model.profile_model import UserRoleEnum

profileSeed = SeedMatrix(
    collection_name = Collections.PROFILES,
    data = [
        {
            "_id":"profiles/a5253ebb-9a45-465b-b597-497c3b12cf16",
            "_key":"a5253ebb-9a45-465b-b597-497c3b12cf16",
            "created_at":"2024-03-02T17:46:03.667882",
            "created_by":"profiles/a5253ebb-9a45-465b-b597-497c3b12cf16",
            "updated_at":"2024-03-02T17:46:03.667882",
            "updated_by":"profiles/a5253ebb-9a45-465b-b597-497c3b12cf16",
            "name":"Chin Yan",
            "email":"chinyan@lifelinelab.io",
            "user_role":UserRoleEnum.FREE_MEMBERSHIP
        }
    ]
)