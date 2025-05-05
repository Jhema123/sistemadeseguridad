
import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QSizePolicy, QTabWidget, QSpacerItem, QGroupBox, QFrame, QScrollArea
)
from PyQt5.QtGui import QIcon, QFont
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

        self.btn_alerta = QPushButton()
        self.btn_alerta.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "icons", "alarm.png")))
        self.btn_alerta.setIconSize(QSize(20, 20))
        self.btn_alerta.setFixedSize(30, 30)
        self.btn_alerta.setStyleSheet("background-color: transparent;")
        barra_superior.addWidget(self.btn_alerta)

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
