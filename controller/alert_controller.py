
from PyQt5.QtCore import QTimer
from concurrent.futures import ThreadPoolExecutor
from model.alert_model import AlertasDB

class AlertsController:
    def __init__(self, view):
        self.view = view
        self.executor = ThreadPoolExecutor(max_workers=1)
        AlertasDB.inicializar_bd()
        self.cargar_alertas()

    def cargar_alertas(self):
        future = self.executor.submit(AlertasDB.obtener_alertas)
        future.add_done_callback(self._mostrar_alertas_en_vista)

    def _mostrar_alertas_en_vista(self, future):
        alertas = future.result()
        QTimer.singleShot(0, lambda: self._actualizar_lista(alertas))

    def _actualizar_lista(self, alertas):
        self.view.notifications_display.clear()
        for timestamp, mensaje in alertas:
            self.view.notifications_display.addItem(f"{timestamp} - {mensaje}")
