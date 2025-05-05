
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QLineEdit, QLabel, QListWidgetItem
)
from PyQt5.QtGui import QColor

class CameraView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Cámaras")
        self.setStyleSheet("background-color: #1E1E1E; color: white;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Lista de cámaras
        self.lista_camaras = QListWidget()
        layout.addWidget(QLabel("Cámaras registradas:"))
        layout.addWidget(self.lista_camaras)

        # Formulario de nueva cámara
        form_layout = QHBoxLayout()
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre de la cámara")
        self.input_ruta = QLineEdit()
        self.input_ruta.setPlaceholderText("Índice (0, 1...) o ruta IP")
        self.btn_agregar = QPushButton("Agregar")
        form_layout.addWidget(self.input_nombre)
        form_layout.addWidget(self.input_ruta)
        form_layout.addWidget(self.btn_agregar)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def agregar_item_camara(self, nombre, ruta, tipo, estado, eliminar_callback):
        item = QListWidgetItem(f"{nombre} ({tipo}) - {ruta} [{estado.upper()}]")
        color = QColor("limegreen") if estado == "activa" else QColor("red")
        item.setForeground(color)
        self.lista_camaras.addItem(item)
        item.setData(32, ruta)  # Para eliminar por ruta
        item.setData(33, eliminar_callback)
