from model.alert_conf_model import AlertConfigModel
from view.aler_conf_view import AlertConfigView

class AlertConfigController:
    def __init__(self):
        self.model = AlertConfigModel()
        self.view = AlertConfigView()
        self.view.btn_guardar.clicked.connect(self.guardar_config)
        self.cargar_config()

    def mostrar(self):
        self.view.show()

    def cargar_config(self):
        config = self.model.cargar_config()
        self.view.check_visual.setChecked(config["visual"])
        self.view.check_sonora.setChecked(config["sonora"])
        self.view.check_notificacion.setChecked(config["notificacion"])
        self.view.combo_tonos.setCurrentText(config["tono"])

    def guardar_config(self):
        config_data = {
            "visual": self.view.check_visual.isChecked(),
            "sonora": self.view.check_sonora.isChecked(),
            "notificacion": self.view.check_notificacion.isChecked(),
            "tono": self.view.combo_tonos.currentText()
        }
        self.model.guardar_config(config_data)
        self.view.close()
