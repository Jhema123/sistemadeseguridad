# dashboard_model.py
# dashboard_model.py

from database.connection import mongo_connection

class DashboardModel:
    def __init__(self):
        self.collection = mongo_connection.get_collection("camaras")

    def obtener_estado_camaras(self):
        """
        Retorna la cantidad de cámaras con fallas (estado: 'inactiva').
        """
        try:
            fallas = self.collection.count_documents({"estado": "inactiva"})
            return fallas
        except Exception as e:
            print("Error al obtener estado de cámaras:", e)
            return -1  # Error de conexión o consulta

    def cerrar_conexion(self):
        """
        Este método ya no es necesario con mongo_connection, pero se deja para compatibilidad.
        """
        pass  # Con mongo_connection la conexión se reutiliza
