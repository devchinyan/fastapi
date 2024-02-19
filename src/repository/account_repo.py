from ..database.mongodb.base_repository import BaseRepository
from ..database.mongodb.collection import Collections

class AccountRepository(BaseRepository):
    def __init__(self):
        super().__init__(collection_name=Collections.ACCOUNTS)

accountRepo = AccountRepository()