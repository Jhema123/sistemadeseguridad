import threading
import cv2
import os
import numpy as np
import sip
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from datetime import datetime
from database.base_datos import guardar_deteccion
from reentrenamiento import guardar_imagen
from model.alert_model import AlertasDB
from model.config_grab_model import ConfigGrabModel
from model.grabacion_model import GrabacionesModel  # 👈 Registro de grabaciones

class LiveViewController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)
        self.camaras_activas = {}
        self.alertas_db = AlertasDB()
        self.config_model = ConfigGrabModel()
        self.configuracion_grab = self.config_model.cargar_configuracion()
        self.grabaciones_model = GrabacionesModel()  # 👈 IMPORTANTE
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
                rostros = self.model.detectar_rostros(frame)

                # Procesamiento facial
                for (x, y, w, h) in rostros:
                    rostro = frame[y:y + h, x:x + w]
                    estado = "FOTO"
                    try:
                        rostro_resized = cv2.resize(rostro, (224, 224))
                        entrada = rostro_resized.astype("float32") / 255.0
                        entrada = entrada[np.newaxis, ...]
                        prediccion = self.model.anti_spoofing_model.predict(entrada)[0][0]
                        es_real = prediccion > 0.5

                        if es_real:
                            mensaje = f"✅ Rostro real detectado en cámara {index}"
                            self.alertas_db.insertar_alerta(mensaje)
                            if hasattr(self.view, 'alerts_view') and self.view.alerts_view:
                                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                self.view.alerts_view.agregar_alerta(timestamp, mensaje)

                        estado = "REAL" if es_real else "FOTO"
                        guardar_deteccion(f"{x}_{y}", estado, prediccion)
                        guardar_imagen(rostro, es_real)

                        color = (0, 255, 0) if es_real else (0, 0, 255)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
                        cv2.putText(frame, estado, (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                    except Exception as e:
                        print(f"❌ Error en predicción: {e}")

                # 🎥 Grabación automática
                if self.esta_en_horario():
                    if grabador is None:
                        fourcc = cv2.VideoWriter_fourcc(*'XVID')
                        grabador = cv2.VideoWriter(ruta_salida, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                        inicio_grabacion = datetime.now()
                        print(f"🟢 Grabando cámara {index} en {ruta_salida}")

                        if not ya_registrado:
                            self.grabaciones_model.insertar_grabacion(index, ruta_salida, inicio_grabacion)
                            ya_registrado = True

                    grabador.write(frame)
                else:
                    if grabador:
                        grabador.release()
                        fin_grabacion = datetime.now()
                        self.grabaciones_model.actualizar_fin_grabacion(index, ruta_salida, fin_grabacion)
                        print(f"🛑 Grabación finalizada y registrada: {ruta_salida}")
                        grabador = None
                        ya_registrado = False

                # Mostrar en la vista
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
                pix = QPixmap.fromImage(img)
                pix = pix.scaled(160, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                widget.setPixmap(pix)

            cap.release()
            if grabador:
                grabador.release()
                fin_grabacion = datetime.now()
                self.grabaciones_model.actualizar_fin_grabacion(index, ruta_salida, fin_grabacion)
                print(f"📁 Grabación cerrada correctamente: {ruta_salida}")

        t = threading.Thread(target=run)
        t.daemon = True
        self.camaras_activas[index] = t
        t.start()
