from database.database import get_database
from repositories.message_repo import MessageRepository
import hashlib

def test_get_message():
    db = get_database()
    mr = MessageRepository(db)
    res = mr.get_message('6371c8550dd00910224c6507')
    print(res)

def test_get_all_message():
    print("testing get all message")
    db = get_database()
    mr = MessageRepository(db)
    res = mr.get_all_message()
    for d in res:
        r = hashlib.sha256(str(d['_id']).encode('utf-8')).hexdigest()
        print(r)