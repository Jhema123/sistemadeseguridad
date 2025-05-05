
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
import sys

from view.config_grab_view import ConfigGrabView
from controller.config_grab_controller import ConfigGrabController


def main():
    app = QApplication(sys.argv)
    ventana = QWidget()
    ventana.setWindowTitle("Test - Configuración de Grabación")

    layout = QVBoxLayout(ventana)
    vista = ConfigGrabView()
    controlador = ConfigGrabController(vista)

    layout.addWidget(vista)
    ventana.setLayout(layout)
    ventana.resize(400, 300)
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
