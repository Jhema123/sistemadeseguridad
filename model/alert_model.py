
from database.connection import mongo_connection
from datetime import datetime

class AlertasDB:
    def __init__(self):
        self.collection = mongo_connection.get_collection("alertas")

    def insertar_alerta(self, mensaje):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.collection.insert_one({
            "timestamp": timestamp,
            "mensaje": mensaje
        })

    def obtener_alertas(self):
        resultados = self.collection.find().sort("_id", -1)
        return [(doc["timestamp"], doc["mensaje"]) for doc in resultados]
