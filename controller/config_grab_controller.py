
from model.config_grab_model import ConfigGrabModel
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer
from datetime import datetime

class ConfigGrabController:
    def __init__(self, view):
        self.view = view
        self.model = ConfigGrabModel()

        # Conectar botón de guardar
        self.view.btn_guardar.clicked.connect(self.guardar_configuracion)

        # Cargar configuración existente al iniciar
        self.config = self.model.cargar_configuracion()
        if self.config:
            self.view.establecer_configuracion(self.config)

        # Activar verificación de horario
        self.timer = QTimer()
        self.timer.timeout.connect(self.verificar_grabacion)
        self.timer.start(60000)  # Cada minuto

    def guardar_configuracion(self):
        config = self.view.obtener_configuracion()
        print("🔧 CONFIG A GUARDAR:", config)  # <--- este debe aparecer en consola
        self.model.guardar_configuracion(config)
        self.config = config
        QMessageBox.information(self.view, "Guardado", "✅ Configuración guardada correctamente.")


    def verificar_grabacion(self):
        if not self.config:
            return

        ahora = datetime.now()
        dia_actual = ahora.strftime("%A")
        hora_actual = ahora.strftime("%H:%M")

        dias = self.config.get("dias", [])
        hora_inicio = self.config.get("hora_inicio", "")
        hora_fin = self.config.get("hora_fin", "")

        if dia_actual in dias and hora_inicio <= hora_actual <= hora_fin:
            print("🟢 Grabación activada automáticamente")
        else:
            print("⚪ Grabación fuera del horario")
