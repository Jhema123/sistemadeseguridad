
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout, QLineEdit,
    QPushButton, QGridLayout, QMessageBox, QGroupBox
)
from PyQt5.QtCore import Qt


class ConfigGrabView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1E1E1E; color: white;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Configuración de Grabación")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        layout.addSpacing(10)

        layout.addWidget(QLabel("Seleccionar días:"))

        dias_group = QGroupBox()
        dias_layout = QGridLayout(dias_group)
        self.checkboxes_dias = []

        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        tags = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        for i, (nombre, tag) in enumerate(zip(dias, tags)):
            chk = QCheckBox(nombre)
            chk.setProperty("tag", tag)
            chk.setStyleSheet("color: white;")
            dias_layout.addWidget(chk, 0, i)
            self.checkboxes_dias.append(chk)

        layout.addWidget(dias_group)

        layout.addSpacing(10)

        layout.addWidget(QLabel("Hora de inicio (HH:MM):"))
        self.hora_inicio = QLineEdit("08:00")
        self.hora_inicio.setFixedWidth(100)
        layout.addWidget(self.hora_inicio)

        layout.addWidget(QLabel("Hora de fin (HH:MM):"))
        self.hora_fin = QLineEdit("18:00")
        self.hora_fin.setFixedWidth(100)
        layout.addWidget(self.hora_fin)

        self.btn_guardar = QPushButton("Guardar configuración")
        self.btn_guardar.setStyleSheet("background-color: #00A8F3; color: white; height: 30px;")
        self.btn_guardar.setFixedWidth(180)
        layout.addWidget(self.btn_guardar, alignment=Qt.AlignLeft)

        layout.addStretch()

    def obtener_configuracion(self):
        dias_seleccionados = [cb.property("tag") for cb in self.checkboxes_dias if cb.isChecked()]
        return {
            "dias": dias_seleccionados,
            "hora_inicio": self.hora_inicio.text(),
            "hora_fin": self.hora_fin.text()
        }

    def establecer_configuracion(self, config):
        dias = config.get("dias", [])
        for cb in self.checkboxes_dias:
            cb.setChecked(cb.property("tag") in dias)
        self.hora_inicio.setText(config.get("hora_inicio", "08:00"))
        self.hora_fin.setText(config.get("hora_fin", "18:00"))
