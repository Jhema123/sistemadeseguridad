
from PyQt5.QtCore import QTimer
from model.config_model import CameraModel
from view.config_view import CameraView

class CameraController:
    def __init__(self):
        self.model = CameraModel()
        self.view = CameraView()
        self.view.btn_agregar.clicked.connect(self.agregar_camara)
        self.actualizar_lista()
        self.iniciar_verificacion()

    def mostrar(self):
        self.view.show()

    def actualizar_lista(self):
        self.view.lista_camaras.clear()
        camaras = self.model.listar_camaras()
        for cam in camaras:
            estado = self.model.verificar_estado_camara(cam["ruta"])
            self.model.actualizar_estado(cam["ruta"], estado)
            self.view.agregar_item_camara(
                cam["nombre"], cam["ruta"], cam["tipo"], estado,
                lambda ruta=cam["ruta"]: self.eliminar_camara(ruta)
            )

    def agregar_camara(self):
        nombre = self.view.input_nombre.text().strip()
        ruta = self.view.obtener_ruta_seleccionada()
        if not nombre or not ruta:
            return
        tipo = "USB"
        print(f"➡ Agregando cámara: {nombre} ({ruta})")
        self.model.agregar_camara(nombre, tipo, ruta)
        self.actualizar_lista()


    def eliminar_camara(self, ruta):
        self.model.eliminar_camara(ruta)
        self.actualizar_lista()

    def iniciar_verificacion(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_lista)
        self.timer.start(10000)  # Verifica cada 10 segundos

    def obtener_total_inactivas(self):
        return self.model.contar_camaras_inactivas()