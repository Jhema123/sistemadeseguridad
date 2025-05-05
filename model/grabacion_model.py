from pymongo import MongoClient
from datetime import datetime, timedelta

class GrabacionesModel:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["vigilancia_ia"]
        self.collection = self.db["grabaciones"]

    def obtener_grabaciones_por_camara_y_rango(self, camara, inicio, fin):
        return list(self.collection.find({
            "camara": camara,
            "$or": [
                {"inicio": {"$lte": fin}, "fin": {"$gte": inicio}}
            ]
        }))

    def obtener_grabaciones_por_camara_y_fecha_exacta(self, camara, fecha):
        inicio = datetime.combine(fecha, datetime.min.time())
        fin = inicio + timedelta(days=1)
        return list(self.collection.find({
            "camara": camara,
            "inicio": {"$gte": inicio, "$lt": fin}
        }))


    def insertar_grabacion(self, camara, ruta, inicio):
        self.collection.insert_one({
            "camara": camara,
            "ruta": ruta,
            "inicio": inicio,
            "fin": None,
            "estado": "en_progreso"
        })

    def actualizar_fin_grabacion(self, camara, ruta, fin):
        self.collection.update_one(
            {"camara": camara, "ruta": ruta},
            {"$set": {"fin": fin, "estado": "finalizada"}}
        )
