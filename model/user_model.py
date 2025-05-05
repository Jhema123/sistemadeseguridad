from database.connection import mongo_connection


class UserModel:
    def __init__(self):
        self.collection = mongo_connection.get_collection("usuarios")

    def validar_usuario(self, usuario, contrasena):
        # ❗️ Este método debe retornar el DOCUMENTO del usuario, no un booleano
        return self.collection.find_one({
            "usuario": usuario,
            "contrasena": contrasena
        })

    def crear_usuario(self, usuario, contrasena):
        if not self.collection.find_one({"usuario": usuario}):
            self.collection.insert_one({"usuario": usuario, "contrasena": contrasena})
            return True
        return False
    
    def obtener_usuario(self, user_id):
        return self.collection.find_one({"id_usu": user_id})

    def actualizar_usuario(self, user_id, nombre, nueva_contrasena=None):
        update = {"nombre": nombre}
        if nueva_contrasena:
            update["contrasena"] = nueva_contrasena
        self.collection.update_one({"id_usu": user_id}, {"$set": update})

