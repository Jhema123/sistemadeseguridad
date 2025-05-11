from database.connection import mongo_connection

class AlertConfigModel:
    def __init__(self):
        self.collection = mongo_connection.get_collection("alert_config")

    def cargar_config(self):
        config = self.collection.find_one({})
        if config:
            return {
                "visual": config.get("visual", True),
                "sonora": config.get("sonora", True),
                "notificacion": config.get("notificacion", True),
                "tono": config.get("tono", "default.wav")
            }
        else:
            default_config = {
                "visual": True,
                "sonora": True,
                "notificacion": True,
                "tono": "default.wav"
            }
            self.collection.insert_one(default_config)
            return default_config

    def guardar_config(self, config_data):
        self.collection.delete_many({})
        self.collection.insert_one(config_data)
