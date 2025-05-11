
from PyQt5.QtCore import QObject, pyqtSignal
import cv2
import os
import numpy as np
import sip
import time
from datetime import datetime
import torch

class CameraWorker(QObject):
    frame_ready = pyqtSignal(object, np.ndarray)
    finished = pyqtSignal()

    def __init__(self, index, widget, model, yolo_model, anti_spoof_model, grabacion_model, config_grab):
        super().__init__()
        self.index = index
        self.widget = widget
        self.model = model
        self.yolo_model = yolo_model
        self.anti_spoof_model = anti_spoof_model
        self.grabacion_model = grabacion_model
        self.config = config_grab
        self.running = True
        self.rostro_cache = {}

    def esta_en_horario(self):
        from model.config_grab_model import ConfigGrabModel
        config_model = ConfigGrabModel()
        config = config_model.cargar_configuracion()
        if not config:
            return False

        ahora = datetime.now()
        dia = ahora.strftime("%A")
        hora = ahora.strftime("%H:%M")
        dias = config.get("dias", [])
        inicio = config.get("hora_inicio", "00:00")
        fin = config.get("hora_fin", "23:59")
        return dia in dias and inicio <= hora <= fin

    def run(self):
        cap = self.model.iniciar_captura(self.index)
        if cap is None or not cap.isOpened():
            print(f"❌ No se pudo iniciar la cámara {self.index}")
            self.finished.emit()
            return

        self.yolo_model.to("cuda" if torch.cuda.is_available() else "cpu")

        nombre_archivo = f"grabacion_cam_{self.index}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
        ruta_salida = os.path.join("grabaciones", nombre_archivo)
        os.makedirs("grabaciones", exist_ok=True)

        grabador = None
        inicio_grabacion = None
        ya_registrado = False
        frame_count = 0

        while cap.isOpened() and self.running:
            ret, frame = cap.read()
            if not ret or not self.widget or sip.isdeleted(self.widget):
                break

            frame = cv2.flip(frame, 1)
            resized_frame = cv2.resize(frame, (640, 480))

            if frame_count % 3 == 0:
                self.detectar_personas(resized_frame)
                rostros = self.model.detectar_rostros(resized_frame)
                self.procesar_rostros_con_cache(rostros, frame)

            frame_count += 1

            if self.esta_en_horario():
                if grabador is None:
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    grabador = cv2.VideoWriter(ruta_salida, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                    inicio_grabacion = datetime.now()
                    if not ya_registrado:
                        self.grabacion_model.insertar_grabacion(self.index, ruta_salida, inicio_grabacion)
                        ya_registrado = True
                grabador.write(frame)
            else:
                if grabador:
                    grabador.release()
                    self.grabacion_model.actualizar_fin_grabacion(self.index, ruta_salida, datetime.now())
                    grabador = None
                    ya_registrado = False

            self.frame_ready.emit(self.widget, frame)
            time.sleep(0.03)

        cap.release()
        if grabador:
            grabador.release()
            self.grabacion_model.actualizar_fin_grabacion(self.index, ruta_salida, datetime.now())
        self.finished.emit()

    def detectar_personas(self, frame):
        try:
            results = self.yolo_model(frame)[0]
            for box in results.boxes:
                cls = int(box.cls[0])
                if self.yolo_model.names[cls] == "person":
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    persona = frame[y1:y2, x1:x2]
                    os.makedirs("dataset/images_yolo", exist_ok=True)
                    filename = f"persona_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]}.jpg"
                    cv2.imwrite(os.path.join("dataset/images_yolo", filename), persona)
        except Exception as e:
            print(f"❌ Error al detectar personas: {e}")

    def procesar_rostros_con_cache(self, rostros, frame):
        ahora = time.time()
        for (x, y, w, h) in rostros:
            try:
                rostro_id = f"{x}_{y}_{w}_{h}"
                tiempo_ultimo = self.rostro_cache.get(rostro_id, 0)

                if ahora - tiempo_ultimo < 2.0:
                    continue

                rostro = frame[y:y+h, x:x+w]
                rostro_resized = cv2.resize(rostro, (224, 224))
                entrada = rostro_resized.astype("float32") / 255.0
                entrada = entrada[np.newaxis, ...]

                pred = self.anti_spoof_model.predict(entrada)[0][0]
                es_real = pred > 0.5
                estado = "REAL" if es_real else "FOTO"
                color = (0, 255, 0) if es_real else (0, 0, 255)

                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
                cv2.putText(frame, estado, (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                self.rostro_cache[rostro_id] = ahora

            except Exception as e:
                print(f"❌ Error en anti-spoofing: {e}")

    def stop(self):
        self.running = False
