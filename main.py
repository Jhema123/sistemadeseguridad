import sys
from PyQt5.QtWidgets import QApplication
from view.login_view import LoginView
from model.user_model import UserModel
from controller.login_controller import LoginController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    vista = LoginView()
    modelo = UserModel()
    controlador = LoginController(vista, modelo)
    vista.show()
    sys.exit(app.exec_())
