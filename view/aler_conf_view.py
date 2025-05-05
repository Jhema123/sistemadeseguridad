from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton, QComboBox

class AlertConfigView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración de Alertas")
        self.setStyleSheet("background-color: #2b2b2b; color: white;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.check_visual = QCheckBox("Alerta visual")
        self.check_sonora = QCheckBox("Alerta sonora")
        self.check_notificacion = QCheckBox("Notificación por cámara inactiva")

        self.combo_tonos = QComboBox()
        self.combo_tonos.addItems(["default.wav", "alerta1.wav", "alerta2.wav"])

        self.btn_guardar = QPushButton("Guardar configuración")
        layout.addWidget(QLabel("Configuración de Alertas"))
        layout.addWidget(self.check_visual)
        layout.addWidget(self.check_sonora)
        layout.addWidget(self.check_notificacion)
        layout.addWidget(QLabel("Tono de alerta:"))
        layout.addWidget(self.combo_tonos)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)
