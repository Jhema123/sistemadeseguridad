import threading
import cv2
import os
import numpy as np
import sip
import torch
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from datetime import datetime
from database.base_datos import guardar_deteccion
from reentrenamiento import guardar_imagen
from model.alert_model import AlertasDB
from model.config_grab_model import ConfigGrabModel
from model.grabacion_model import GrabacionesModel
from ultralytics import YOLO

class LiveViewController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)
        self.camaras_activas = {}
        self.alertas_db = AlertasDB()
        self.config_model = ConfigGrabModel()
        self.configuracion_grab = self.config_model.cargar_configuracion()
        self.yolo_model = YOLO("yolov8s.pt")
        self.grabaciones_model = GrabacionesModel()
        self.inicializar()

    def inicializar(self):
        indices = self.model.detectar_camaras()
        self.view.populate_camera_tree(indices)

    def esta_en_horario(self):
        if not self.configuracion_grab:
            return False
        ahora = datetime.now()
        dia = ahora.strftime("%A")
        hora = ahora.strftime("%H:%M")
        dias = self.configuracion_grab.get("dias", [])
        inicio = self.configuracion_grab.get("hora_inicio", "00:00")
        fin = self.configuracion_grab.get("hora_fin", "23:59")
        return dia in dias and inicio <= hora <= fin

    def assign_camera(self, index, widget):
        def run():
            cap = self.model.iniciar_captura(index)
            if cap is None or not cap.isOpened():
                print(f"❌ No se pudo iniciar la cámara {index}")
                return

            self.yolo_model.to("cuda" if torch.cuda.is_available() else "cpu")

            nombre_archivo = f"grabacion_cam_{index}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
            ruta_salida = os.path.join("grabaciones", nombre_archivo)
            os.makedirs("grabaciones", exist_ok=True)

            grabador = None
            inicio_grabacion = None
            ya_registrado = False

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret or not widget or sip.isdeleted(widget):
                    break

                frame = cv2.flip(frame, 1)
                self.detectar_personas(frame)
                rostros = self.model.detectar_rostros(frame)
                self.procesar_rostros(rostros, frame, index)

                grabador, inicio_grabacion, ya_registrado = self.grabar_video_si_es_necesario(
                    frame, grabador, index, ruta_salida, inicio_grabacion, ya_registrado
                )

                self.mostrar_frame(widget, frame)

            cap.release()
            if grabador:
                grabador.release()
                self.grabaciones_model.actualizar_fin_grabacion(index, ruta_salida, datetime.now())
                print(f"📁 Grabación cerrada correctamente: {ruta_salida}")

        t = threading.Thread(target=run)
        t.daemon = True
        self.camaras_activas[index] = t
        t.start()

    def detectar_personas(self, frame):
        try:
            results = self.yolo_model(frame)[0]
            for box in results.boxes:
                cls = int(box.cls[0])
                if self.yolo_model.names[cls] == "person":
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    margin = 0.2
                    w, h = x2 - x1, y2 - y1
                    x1 = max(0, int(x1 - w * margin))
                    y1 = max(0, int(y1 - h * margin))
                    x2 = min(frame.shape[1], int(x2 + w * margin))
                    y2 = min(frame.shape[0], int(y2 + h * margin))
                    persona = frame[y1:y2, x1:x2]
                    os.makedirs("dataset/images_yolo", exist_ok=True)
                    filename = f"persona_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]}.jpg"
                    cv2.imwrite(os.path.join("dataset/images_yolo", filename), persona)
        except Exception as e:
            print(f"❌ Error al detectar personas: {e}")

    def procesar_rostros(self, rostros, frame, index):
        for (x, y, w, h) in rostros:
            try:
                rostro = frame[y:y+h, x:x+w]
                rostro_resized = cv2.resize(rostro, (224, 224))
                entrada = rostro_resized.astype("float32") / 255.0
                entrada = entrada[np.newaxis, ...]

                pred = self.model.anti_spoofing_model.predict(entrada)[0][0]
                es_real = pred > 0.5

                estado = "REAL" if es_real else "FOTO"
                color = (0, 255, 0) if es_real else (0, 0, 255)

                guardar_deteccion(f"{x}_{y}", estado, pred)
                guardar_imagen(rostro, es_real)

                carpeta = "dataset/reentrenamiento/real" if es_real else "dataset/reentrenamiento/foto"
                os.makedirs(carpeta, exist_ok=True)
                filename = f"rostro_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]}.jpg"
                cv2.imwrite(os.path.join(carpeta, filename), rostro)

                if es_real:
                    mensaje = f"✅ Rostro real detectado en cámara {index}"
                    self.alertas_db.insertar_alerta(mensaje)
                    if hasattr(self.view, 'alerts_view') and self.view.alerts_view:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.view.alerts_view.agregar_alerta(timestamp, mensaje)

                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
                cv2.putText(frame, estado, (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            except Exception as e:
                print(f"❌ Error en anti-spoofing: {e}")

    def grabar_video_si_es_necesario(self, frame, grabador, index, ruta_salida, inicio, ya_registrado):
        if self.esta_en_horario():
            if grabador is None:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                grabador = cv2.VideoWriter(ruta_salida, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                inicio = datetime.now()
                print(f"🟢 Grabando cámara {index} en {ruta_salida}")
                if not ya_registrado:
                    self.grabaciones_model.insertar_grabacion(index, ruta_salida, inicio)
                    ya_registrado = True
            grabador.write(frame)
        else:
            if grabador:
                grabador.release()
                self.grabaciones_model.actualizar_fin_grabacion(index, ruta_salida, datetime.now())
                print(f"🛑 Grabación finalizada: {ruta_salida}")
                grabador = None
                ya_registrado = False
        return grabador, inicio, ya_registrado

    def mostrar_frame(self, widget, frame):
        try:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
            pix = QPixmap.fromImage(img)
            pix = pix.scaled(160, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            widget.setPixmap(pix)
        except Exception as e:
            print(f"❌ Error al mostrar frame: {e}")
            print(f"❌ Error al mostrar frame: {e}")