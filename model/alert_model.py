
from pymongo import MongoClient
from datetime import datetime

class AlertasDB:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="vigilancia_ia", collection_name="alertas"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insertar_alerta(self, mensaje):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.collection.insert_one({
            "timestamp": timestamp,
            "mensaje": mensaje
        })

    def obtener_alertas(self):
        resultados = self.collection.find().sort("_id", -1)
        return [(doc["timestamp"], doc["mensaje"]) for doc in resultados]
