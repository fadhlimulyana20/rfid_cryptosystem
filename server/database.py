from pymongo import MongoClient

def get_database():
    connection_string = "mongodb://root:password@localhost:27017"
    client = MongoClient(connection_string)
    return client['rfid_cryptosystem']

if __name__ == "__main__":
    dbname = get_database()