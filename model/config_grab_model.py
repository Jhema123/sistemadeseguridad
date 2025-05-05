
from pymongo import MongoClient

class ConfigGrabModel:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="vigilancia_ia", collection_name="Config_grab"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def guardar_configuracion(self, config):
        self.collection.delete_many({})  # Solo mantener una configuración
        self.collection.insert_one(config)

    def cargar_configuracion(self):
        doc = self.collection.find_one()
        if doc:
            doc.pop("_id", None)
            return doc
        return None
