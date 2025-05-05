
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLabel, QComboBox, QListWidgetItem
)
from PyQt5.QtCore import Qt
from model.alert_model import AlertasDB

class AlertView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1E1E1E; color: white;")
        self.init_ui()
        self.cargar_alertas()  # 🔁 Cargar al iniciar

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        sidebar = QVBoxLayout()
        sidebar.setContentsMargins(10, 10, 10, 10)
        sidebar.setSpacing(10)
        
        label_cameras = QLabel("🎥 Cámaras")
        label_cameras.setStyleSheet("font-weight: bold;")
        sidebar.addWidget(label_cameras)

        self.camera_list = QListWidget()
        self.camera_list.setStyleSheet("background-color: #444; color: white;")
        self.camera_list.setFixedHeight(200)
        sidebar.addWidget(self.camera_list)


        alert_panel = QVBoxLayout()
        alert_panel.setContentsMargins(10, 10, 10, 10)
        alert_panel.setSpacing(10)

        title = QLabel("📢 Alertas en Tiempo Real")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        alert_panel.addWidget(title)

        self.notifications_display = QListWidget()
        self.notifications_display.setStyleSheet("background-color: #333; color: white; border: 1px solid gray;")
        alert_panel.addWidget(self.notifications_display)

        main_layout.addLayout(sidebar, 1)
        main_layout.addLayout(alert_panel, 3)

    def agregar_alerta(self, timestamp, mensaje):
        self.notifications_display.insertItem(0, f"{timestamp} - {mensaje}")

    def cargar_alertas(self):
        db = AlertasDB()
        alertas = db.obtener_alertas()
        self.notifications_display.clear()
        for timestamp, mensaje in alertas:
            self.notifications_display.addItem(f"{timestamp} - {mensaje}")
