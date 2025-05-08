
import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QSizePolicy, QTabWidget, QSpacerItem, QGroupBox, QFrame, QScrollArea, QColorDialog
)
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import Qt, QTimer, QTime, QSize

class DashboardView(QWidget):
    def __init__(self, controller, usuario):
        super().__init__()
        self.controller = controller
        self.usuario = usuario
        self.setGeometry(100, 50, 1200, 800)
        self.label_usuario = QLabel(f"👤 Usuario: {self.usuario}")
        self.label_usuario.setStyleSheet("font-size: 10pt; color: white;")

        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: #121212; color: white;")
        main_layout = QVBoxLayout(self)

        # --- Barra superior ---
        barra_superior = QHBoxLayout()
        barra_superior.setSpacing(10)

        self.btn_add_tab = QPushButton("+")
        self.btn_add_tab.setFixedSize(30, 30)
        self.btn_add_tab.setStyleSheet("background-color: transparent; color: white;")
        self.btn_add_tab.clicked.connect(self.controller.agregar_pestana)
        barra_superior.addWidget(self.btn_add_tab)

        barra_superior.addStretch()

        self.notif_view = NotificationView()
        self.notif_view.mousePressEvent = self.abrir_configuracion_camaras
        barra_superior.addWidget(self.notif_view)

        barra_superior.addWidget(self.label_usuario)

        self.lbl_hora = QLabel()
        self.lbl_hora.setStyleSheet("font-size: 10pt; color: white;")
        barra_superior.addWidget(self.lbl_hora)

        for symbol, handler in [("🗕", self.showMinimized), ("🗖", self.showMaximized), ("✕", self.close)]:
            btn = QPushButton(symbol)
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("background-color: transparent; color: white;")
            btn.clicked.connect(handler)
            barra_superior.addWidget(btn)

        top_frame = QFrame()
        top_frame.setLayout(barra_superior)
        main_layout.addWidget(top_frame)

        # --- Pestañas ---
        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.controller.cerrar_pestana)
        self.tabs.currentChanged.connect(self.controller.detectar_click_tab)
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background: #1e1e1e;
                color: #ccc;
                padding: 10px;
                border: 1px solid #444;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #2d2d2d;
                color: white;
                font-weight: bold;
            }
            QTabWidget::pane {
                border-top: 2px solid #444;
                top: -0.5em;
            }
        """)
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        # --- Temporizadores ---
        self.actualizar_hora()
        reloj_timer = QTimer(self)
        reloj_timer.timeout.connect(self.actualizar_hora)
        reloj_timer.start(1000)

        alerta_timer = QTimer(self)
        alerta_timer.timeout.connect(self.controller.verificar_alertas)
        alerta_timer.start(10000)

    def actualizar_hora(self):
        self.lbl_hora.setText(QTime.currentTime().toString("HH:mm:ss"))

    def insertar_pestana(self, widget, titulo):
        self.tabs.insertTab(self.tabs.count(), widget, titulo)
        self.tabs.setCurrentIndex(self.tabs.count() - 1)

    def eliminar_pestana(self, index):
        self.tabs.removeTab(index)

    def abrir_configuracion_camaras(self, event):
        if event.button() == Qt.LeftButton:
            self.controller.abrir_config()


    def get_tab_index(self):
        return self.tabs.currentIndex()

    def get_tab_text(self, index):
        return self.tabs.tabText(index)

    def set_tab_widget(self, index, widget, titulo):
        self.tabs.removeTab(index)
        self.tabs.insertTab(index, widget, titulo)
        self.tabs.setCurrentIndex(index)
        
    def mostrar_nombre_usuario(self, nombre):
        self.label_usuario.setText(f"👤 Usuario: {nombre}")

    def actualizar_notificacion_camaras(self, cantidad):
        if hasattr(self, 'notif_view'):
            self.notif_view.contador.setText(str(cantidad))
            self.notif_view.contador.setVisible(cantidad > 0)
            self.notif_view.setVisible(cantidad > 0)

class NotificationView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("#3A3A3A"))
        self.setPalette(palette)

        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)

        self.icono = QLabel("🔔")
        self.icono.setStyleSheet("color: white; font-size: 14px;")

        self.contador = QLabel("0")
        self.contador.setStyleSheet("color: white; font-size: 14px;")
        self.contador.setVisible(False)

        self.texto = QLabel("Cámaras con fallas")
        self.texto.setStyleSheet("color: white; font-size: 14px;")

        layout.addWidget(self.icono)
        layout.addWidget(self.contador)
        layout.addWidget(self.texto)

        self.setLayout(layout)
        self.setVisible(False)
