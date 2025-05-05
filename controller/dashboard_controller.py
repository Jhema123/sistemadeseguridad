from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import os
from pymongo import MongoClient
from view.dashboard_view import DashboardView
from view.liveview_view import LiveView
from view.alert_view import AlertView
from view.recording_view import RecordingView
from view.config_view import CameraView
from model.dashboard_model import DashboardModel
from controller.liveview_controller import LiveViewController
from controller.liveview_controller import LiveViewController
from model.liveview_model import LiveViewModel
from view.liveview_view import LiveView
from view.config_grab_view import ConfigGrabView
from controller.config_grab_controller import ConfigGrabController
from model.config_grab_model import ConfigGrabModel
from controller.recording_controller import RecordingController
from controller.alert_conf_controller import AlertConfigController
from controller.user_conf_controller import UserConfigController
from controller.config_controller import CameraController



class DashboardController:
    def __init__(self, usuario,user_id):
        self.user_id = user_id
        self.modelo = DashboardModel()
        self.view = DashboardView(self, usuario)  # 👈 AQUÍ: self.view, no self.vista
        self.view.tabs.addTab(self.crear_menu(), "New")
        self.view.show()

    def crear_menu(self):
        contenedor = QWidget()
        layout = QVBoxLayout(contenedor)

        layout.addWidget(self.crear_grupo("Operation", [
            ("Live View", "liveview.png", self.abrir_liveview),
            ("Event", "alarm.png", self.abrir_alertas)
        ]))
        layout.addWidget(self.crear_grupo("Search", [
            ("Playback", "playback.png", self.abrir_recording)
        ]))
        layout.addWidget(self.crear_grupo("Configuration", [
            ("Devices", "devices.png", self.abrir_configdev),
            ("Event Config", "alarmcfg.png", self.abrir_config_alertas),
            ("User", "user.png", self.abrir_config_usuario),
            ("Device Configuracion", "devicecfg.png", self.abrir_config)
        ]))
        return contenedor

    def crear_grupo(self, titulo, botones):
        group = QGroupBox(titulo)
        layout = QHBoxLayout()
        icon_path = os.path.join(os.path.dirname(__file__), "../view/icons")
        for texto, icono, funcion in botones:
            btn = QPushButton(texto)
            btn.setIcon(QIcon(os.path.join(icon_path, icono)))
            btn.setIconSize(QSize(48, 48))
            btn.setMinimumSize(150, 100)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.setStyleSheet("font-size: 10pt; padding: 10px; color: white; text-align: left;")
            btn.clicked.connect(funcion)
            layout.addWidget(btn)
        group.setLayout(layout)
        return group

    def agregar_pestana(self):
        # Agrega una nueva pestaña con contenido de selección (menu)
        nueva = self.crear_menu()
        index = self.view.tabs.currentIndex()
        self.view.tabs.insertTab(index + 1, nueva, "New")
        self.view.tabs.setCurrentIndex(index + 1)

    def detectar_click_tab(self, index):
        # Si el usuario hace clic en 'New', no hacemos nada
        pass

    def abrir_en_pestana(self, widget: QWidget, titulo: str):
        index = self.view.tabs.currentIndex()
        if self.view.tabs.tabText(index) == "New":
            self.view.tabs.removeTab(index)
            self.view.tabs.insertTab(index, widget, titulo)
            self.view.tabs.setCurrentIndex(index)
        else:
            self.view.tabs.insertTab(self.view.tabs.count(), widget, titulo)
            self.view.tabs.setCurrentIndex(self.view.tabs.count() - 1)

    # Métodos públicos llamados por botones
    def abrir_liveview(self):
        vista = LiveView(None)  # Primero crea la vista sin controlador
        modelo = LiveViewModel()  # Tu clase de modelo, puede ser vacía si no necesitas lógica
        controlador = LiveViewController(modelo, vista)
        vista.controller = controlador  # Asignar el controlador a la vista
        self.abrir_en_pestana(vista, "Live View")

    def abrir_alertas(self):
        self.abrir_en_pestana(AlertView(), "Event")

    def abrir_recording(self):
        self.recording_controller = RecordingController()  # 👈 mantener referencia
        self.abrir_en_pestana(self.recording_controller.mostrar(), "Playback")

    def abrir_config(self):
        self.lista_camaras_ctrl = CameraController()
        self.view.insertar_pestana(self.lista_camaras_ctrl.view, "📷 Cámaras")

    def abrir_configdev(self):
        vista = ConfigGrabView()
        self.config_grab_controlador = ConfigGrabController(vista)  # ✅ referencia persistente
        self.abrir_en_pestana(vista, "Configuración de Grabación")

    def abrir_config_alertas(self):
        self.alertas_controller = AlertConfigController()
        self.alertas_controller.mostrar()

    def abrir_config_usuario(self):
        self.config_user = UserConfigController(self.user_id)
        self.config_user.mostrar()

    def cerrar_pestana(self, index):
        if self.view.tabs.tabText(index) != "+":
            self.view.tabs.removeTab(index)

    def verificar_alertas(self):
        try:
            cliente = MongoClient("mongodb://localhost:27017/")
            db = cliente["vigilancia_ia"]
            camaras = db["camaras"]
            fallas = camaras.count_documents({"estado": False})
            if fallas > 0:
                self.view.btn_alerta.setStyleSheet("background-color: #cc0000; border-radius: 4px;")
                self.view.btn_alerta.setToolTip(f"{fallas} cámara(s) con fallas")
            else:
                self.view.btn_alerta.setStyleSheet("background-color: transparent;")
                self.view.btn_alerta.setToolTip("Sin alertas")
        except:
            self.view.btn_alerta.setStyleSheet("background-color: #ff9900;")
            self.view.btn_alerta.setToolTip("Error al verificar alertas")
