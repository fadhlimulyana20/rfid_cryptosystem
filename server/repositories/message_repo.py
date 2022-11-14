from pymongo import MongoClient
from pymongo.database import Database
from models.message import MessageEncryptedData, MessageEncryptedDataStored
from database.database import get_database
from bson.objectid import ObjectId

class MessageRepository():
    def __init__(self, db: Database) -> None:
        self.db = db

    def add_message(self, data: MessageEncryptedData) -> MessageEncryptedData:
        col = self.db['message']
        r = col.insert_one(data.dict())
        return data
    
    def get_message(self, id):
        col = self.db['message']
        res = col.find_one({"_id": ObjectId(id)})
        return res
    
    def get_all_message(self):
        col = self.db['message']
        res = col.find()
        return res

if __name__ == "__main__":
    db = get_database()
    mr = MessageRepository(db)
    res = mr.get_message('6371c8550dd00910224c6507')
    print(res)
    