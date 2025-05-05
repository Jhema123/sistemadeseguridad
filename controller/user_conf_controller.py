from model.user_model import UserModel
from view.user_conf_view import UserConfigView
from PyQt5.QtWidgets import QMessageBox

class UserConfigController:
    def __init__(self, user_id):
        self.user_id = user_id
        self.model = UserModel()
        self.view = UserConfigView()
        self.view.btn_guardar.clicked.connect(self.guardar_cambios)
        self.cargar_datos()

    def mostrar(self):
        self.view.show()

    def cargar_datos(self):
        usuario = self.model.obtener_usuario(self.user_id)
        if usuario:
            self.view.nombre_input.setText(usuario.get("nombre", ""))

    def guardar_cambios(self):
        nombre = self.view.nombre_input.text()
        nueva = self.view.pass_input.text()
        confirmar = self.view.pass_confirm.text()

        if nueva and nueva != confirmar:
            QMessageBox.warning(self.view, "Error", "Las contraseñas no coinciden.")
            return

        self.model.actualizar_usuario(self.user_id, nombre, nueva if nueva else None)
        QMessageBox.information(self.view, "Éxito", "Datos actualizados correctamente.")
        self.view.close()
