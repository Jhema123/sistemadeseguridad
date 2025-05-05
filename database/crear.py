from pymongo import MongoClient

# Conexión a MongoDB local
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["vigilancia_ia"]
usuarios = db["usuarios"]

# Usuario de prueba
usuario = {
    "usuario": "admin",
    "contrasena": "1234loco"
}

# Insertar solo si no existe
if not usuarios.find_one({"usuario": usuario["usuario"]}):
    usuarios.insert_one(usuario)
    print("✅ Usuario 'admin' creado con contraseña '1234'")
else:
    print("ℹ️ El usuario 'admin' ya existe.")