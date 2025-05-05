from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QLineEdit, QLabel, QListWidgetItem, QComboBox
)
from PyQt5.QtGui import QColor
import cv2

class CameraView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Cámaras")
        self.setStyleSheet("background-color: #1E1E1E; color: white;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.lista_camaras = QListWidget()
        layout.addWidget(QLabel("Cámaras registradas:"))
        layout.addWidget(self.lista_camaras)

        form_layout = QHBoxLayout()
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre de la cámara")

        # 👇 ComboBox en lugar de texto
        self.combo_rutas = QComboBox()
        self.detectar_camaras()

        self.btn_agregar = QPushButton("Agregar")
        form_layout.addWidget(self.input_nombre)
        form_layout.addWidget(self.combo_rutas)
        form_layout.addWidget(self.btn_agregar)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def detectar_camaras(self):
        self.combo_rutas.clear()
        for i in range(10):  # Probar los índices del 0 al 9
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.combo_rutas.addItem(f"Cámara {i}", str(i))
                cap.release()

    def obtener_ruta_seleccionada(self):
        return self.combo_rutas.currentData()

    def agregar_item_camara(self, nombre, ruta, tipo, estado, eliminar_callback):
        item = QListWidgetItem(f"{nombre} ({tipo}) - {ruta} [{estado.upper()}]")
        color = QColor("limegreen") if estado == "activa" else QColor("red")
        item.setForeground(color)
        self.lista_camaras.addItem(item)
        item.setData(32, ruta)
        item.setData(33, eliminar_callback)
