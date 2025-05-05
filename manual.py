import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import torch

# 🔒 Forzar uso exclusivo de GPU (ignorar CPU)
USE_GPU = torch.cuda.is_available()
print("🚀 PyTorch está usando GPU" if USE_GPU else "⚠️ PyTorch usará CPU (puede ser más lento)")

# ✅ Ruta del modelo preentrenado
MODEL_PATH = "anti_spoofing_model.h5"

# ✅ Verificar si el modelo existe
if not os.path.exists(MODEL_PATH):
    print("❌ No se encontró el modelo preentrenado.")
    exit()

# ✅ Cargar el modelo
print("🔄 Cargando modelo existente...")
model = tf.keras.models.load_model(MODEL_PATH)
print("✅ Modelo cargado correctamente.")

# ✅ Configurar generador de datos para reentrenamiento
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

# ✅ Reentrenar el modelo
print("🚀 Iniciando reentrenamiento...")
model.fit(train_generator, validation_data=val_generator, epochs=5)

# ✅ Guardar el modelo mejorado
model.save(MODEL_PATH)
print(f"✅ Modelo reentrenado y guardado en {MODEL_PATH}")
