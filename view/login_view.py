import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout
)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt

class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - EMI-UASC")
        self.setGeometry(100, 50, 1200, 800)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: #0e143e; color: white;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Logo EMI
        logo_path = os.path.join(os.path.dirname(__file__), "icons", "logo.png")
        logo = QLabel()
        logo.setPixmap(QPixmap(logo_path).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        # Texto institucional
        emi_label = QLabel("EMI-UASC")
        emi_label.setFont(QFont("Arial", 28, QFont.Bold))
        emi_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(emi_label)

        lema_label = QLabel("El mejor Sistema de Control y Vigilancia.")
        lema_label.setFont(QFont("Arial", 14))
        lema_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(lema_label)

        # Formulario
        form_layout = QFormLayout()
        form_layout.setFormAlignment(Qt.AlignHCenter)
        form_layout.setContentsMargins(300, 50, 300, 20)

        # Usuario
        self.txt_usuario = QLineEdit()
        self.txt_usuario.setPlaceholderText("Username")
        self.txt_usuario.setFixedHeight(40)
        self.txt_usuario.setStyleSheet("padding-left: 30px;")
        user_icon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "user-icon.png"))
        self.txt_usuario.addAction(user_icon, QLineEdit.LeadingPosition)
        form_layout.addRow(self.txt_usuario)

        # Contraseña
        self.txt_contra = QLineEdit()
        self.txt_contra.setPlaceholderText("Password")
        self.txt_contra.setEchoMode(QLineEdit.Password)
        self.txt_contra.setFixedHeight(40)
        self.txt_contra.setStyleSheet("padding-left: 30px;")
        key_icon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "key-icon.png"))
        self.txt_contra.addAction(key_icon, QLineEdit.LeadingPosition)
        form_layout.addRow(self.txt_contra)

        layout.addSpacing(15)
        layout.addLayout(form_layout)

        # Botón LOGIN
        self.btn_login = QPushButton("LOG IN")
        self.btn_login.setFixedSize(150, 40)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #4e47ff;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3831cc;
            }
        """)
        layout.addWidget(self.btn_login, alignment=Qt.AlignCenter)

        # Enlaces
        links = QLabel('<a style="color:#aaa;">Forgot Password?</a>   <a href="#">Reset</a>')
        links.setAlignment(Qt.AlignCenter)
        links.setStyleSheet("color: #aaa; font-size: 10pt; margin-top: 10px;")
        links.setOpenExternalLinks(True)
        layout.addWidget(links)

        self.setLayout(layout)
