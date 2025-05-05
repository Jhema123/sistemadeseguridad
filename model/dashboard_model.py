# dashboard_model.py

from pymongo import MongoClient

class DashboardModel:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["vigilancia_ia"]

    def obtener_estado_camaras(self):
        """
        Retorna la cantidad de cámaras con fallas (estado: False).
        """
        try:
            camaras = self.db["camaras"]
            fallas = camaras.count_documents({"estado": False})
            return fallas
        except Exception as e:
            print("Error al obtener estado de cámaras:", e)
            return -1  # Error de conexión o consulta

    def cerrar_conexion(self):
        """
        Cierra la conexión con MongoDB.
        """
        self.client.close()
