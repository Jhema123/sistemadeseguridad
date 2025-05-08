from PyQt5.QtWidgets import QMessageBox
from controller.dashboard_controller import DashboardController
from model.user_model import UserModel

class LoginController:
    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo

        # Conectar eventos
        self.vista.btn_login.clicked.connect(self.validar)
        self.vista.txt_usuario.returnPressed.connect(self.validar)
        self.vista.txt_contra.returnPressed.connect(self.validar)

    def validar(self):
        usuario = self.vista.txt_usuario.text()
        contrasena = self.vista.txt_contra.text()

        user_data = self.modelo.validar_usuario(usuario, contrasena)

        if user_data:  # Esto ahora es un dict
            user_id = user_data.get("id_usu")  # ✅ ID personalizado
            nombre = user_data.get("nombre", usuario)

            QMessageBox.information(self.vista, "Acceso concedido", f"¡Bienvenido, {nombre}!")
            self.vista.close()

            dashboard_controller = DashboardController(nombre, user_id )
            self.dashboard = dashboard_controller.view
            self.dashboard.show()
        else:
            QMessageBox.warning(self.vista, "Error", "Usuario o contraseña incorrectos")


