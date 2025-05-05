
import cv2
from pymongo import MongoClient

class CameraModel:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["vigilancia_ia"]
        self.collection = self.db["camaras"]

    def listar_camaras(self):
        return list(self.collection.find())

    def agregar_camara(self, nombre, tipo, ruta):
        if not self.collection.find_one({"ruta": ruta}):
            self.collection.insert_one({
                "nombre": nombre,
                "tipo": tipo,
                "ruta": ruta,
                "estado": "desconocido"
            })

    def eliminar_camara(self, ruta):
        self.collection.delete_one({"ruta": ruta})

    def actualizar_estado(self, ruta, estado):
        self.collection.update_one({"ruta": ruta}, {"$set": {"estado": estado}})

    def verificar_estado_camara(self, ruta):
        try:
            cap = cv2.VideoCapture(int(ruta) if ruta.isdigit() else ruta)
            if cap.isOpened():
                cap.release()
                return "activa"
            return "inactiva"
        except:
            return "inactiva"
