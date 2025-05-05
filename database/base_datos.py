from pymongo import MongoClient
from datetime import datetime

# Conexión a MongoDB local
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["vigilancia_ia"]

def guardar_deteccion(camara, estado, confianza):
    db.detecciones.insert_one({
        "camara": camara,
        "estado": estado,
        "confianza": float(confianza),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def guardar_imagen(imagen, es_real):
    import os
    import cv2

    carpeta = "imagenes_reentrenamiento"
    os.makedirs(carpeta, exist_ok=True)
    nombre = f"img_{'REAL' if es_real else 'FOTO'}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    ruta = os.path.join(carpeta, nombre)
    cv2.imwrite(ruta, imagen)

    db.imagenes_reentrenamiento.insert_one({
        "nombre_archivo": nombre,
        "estado": "REAL" if es_real else "FOTO",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
