
from pymongo import MongoClient
from database.connection import mongo_connection

class ConfigGrabModel:
    def __init__(self):
        self.collection = mongo_connection.get_collection("Config_grab")

    def guardar_configuracion(self, config):
        self.collection.delete_many({})  # Solo mantener una configuración
        self.collection.insert_one(config)

    def cargar_configuracion(self):
        doc = self.collection.find_one()
        if doc:
            doc.pop("_id", None)
            return doc
        return None
