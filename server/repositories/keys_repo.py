from pymongo.database import Database
from models.keys import NTRUKeysReq

class KeysRepository():
    def __init__(self, db: Database) -> None:
        self.db = db

    def add_ntru_key(self, data: NTRUKeysReq):
        col = self.db['keys']
        col.insert_one(data.dict())