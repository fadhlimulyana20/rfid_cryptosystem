from pymongo import MongoClient
from pymongo.database import Database
from models.message import MessageEncryptedData, MessageEncryptedDataStored

class MessageRepository():
    def __init__(self, db: Database) -> None:
        self.db = db

    def add_message(self, data: MessageEncryptedData) -> MessageEncryptedDataStored:
        col = self.db['message']
        r = col.insert_one(data.dict())
        res = data.dict(include={"id": r.inserted_id})
        return MessageEncryptedDataStored(res)