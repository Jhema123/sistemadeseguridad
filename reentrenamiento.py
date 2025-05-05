import os
import time
import threading
import cv2  # ✅ SOLUCIÓN: Importar OpenCV
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ✅ Crear carpetas para almacenar imágenes mal clasificadas
if not os.path.exists("dataset/reentrenamiento/real"):
    os.makedirs("dataset/reentrenamiento/real")
if not os.path.exists("dataset/reentrenamiento/foto"):
    os.makedirs("dataset/reentrenamiento/foto")

def guardar_imagen(face_image, es_real):
    """
    Guarda imágenes en carpetas de 'real' o 'foto' para mejorar el modelo.
    """
    categoria = "real" if es_real else "foto"
    ruta = f"dataset/reentrenamiento/{categoria}/rostro_{time.time()}.jpg"
    cv2.imwrite(ruta, face_image)  # ✅ Usa cv2 para guardar la imagen correctamente
    print(f"💾 Imagen guardada en {ruta}")

def reentrenar_modelo():
    """
    Reentrena el modelo usando imágenes nuevas capturadas.
    """
    global anti_spoofing_model
    print("🔄 Reentrenando el modelo con nuevas imágenes...")

    train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

    train_generator = train_datagen.flow_from_directory(
        "dataset/reentrenamiento",
        target_size=(224, 224),
        batch_size=32,
        class_mode="binary",
        subset="training"
    )

    val_generator = train_datagen.flow_from_directory(
        "dataset/reentrenamiento",
        target_size=(224, 224),
        batch_size=32,
        class_mode="binary",
        subset="validation"
    )

    # Entrenar el modelo con las nuevas imágenes
    anti_spoofing_model.fit(train_generator, validation_data=val_generator, epochs=2)

    # Guardar el modelo mejorado
    anti_spoofing_model.save("anti_spoofing_model.h5")
    print("✅ Modelo reentrenado y guardado.")

    # Cargar el modelo actualizado sin detener el sistema
    anti_spoofing_model = tf.keras.models.load_model("anti_spoofing_model.h5")

# ✅ Programar reentrenamiento cada 1 hora
def iniciar_reentrenamiento_periodico(intervalo=3600):
    while True:
        time.sleep(intervalo)
        reentrenar_modelo()

# ✅ Iniciar en un hilo secundario
threading.Thread(target=iniciar_reentrenamiento_periodico, daemon=True).start()
