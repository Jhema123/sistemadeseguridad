
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class UserConfigView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración de Usuario")
        self.setStyleSheet("background-color: #2b2b2b; color: white;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nuevo nombre")

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Nueva contraseña")
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.pass_confirm = QLineEdit()
        self.pass_confirm.setPlaceholderText("Confirmar contraseña")
        self.pass_confirm.setEchoMode(QLineEdit.Password)

        self.btn_guardar = QPushButton("Guardar cambios")

        layout.addWidget(QLabel("Nombre de usuario:"))
        layout.addWidget(self.nombre_input)
        layout.addWidget(QLabel("Nueva contraseña:"))
        layout.addWidget(self.pass_input)
        layout.addWidget(QLabel("Confirmar contraseña:"))
        layout.addWidget(self.pass_confirm)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)
