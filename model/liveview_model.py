# liveview_model.py

import cv2
import numpy as np
import tensorflow as tf
import torch

class LiveViewModel:
    def __init__(self):
        # Cargar modelo anti-spoofing
        self.anti_spoofing_model = tf.keras.models.load_model("anti_spoofing_model.h5")
        
        # Detector de rostros Haar Cascade
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        # Verificar si se puede usar GPU
        self.use_gpu = torch.cuda.is_available()
        print("🚀 PyTorch está usando GPU" if self.use_gpu else "⚠️ PyTorch usará CPU")

    def detectar_camaras(self, max_cams=10):
        disponibles = []
        for i in range(max_cams):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    disponibles.append(i)
                cap.release()
        return disponibles

    def iniciar_captura(self, index):
        return cv2.VideoCapture(index)

    def detectar_rostros(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rostros = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return rostros
