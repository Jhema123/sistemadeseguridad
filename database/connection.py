from pymongo import MongoClient

class MongoConnection:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="vigilancia_ia"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

mongo_connection = MongoConnection()
