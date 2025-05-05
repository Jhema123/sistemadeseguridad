
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, QWidget, QGridLayout, QLabel, QSizePolicy
)
from PyQt5.QtCore import QSize, Qt


class ToolbarView(QFrame):
    def __init__(self, parent_liveview):
        super().__init__()
        self.parent_liveview = parent_liveview
        self.setStyleSheet("background-color: #2C2C2C; border-top: 1px solid #444;")
        self.setFixedHeight(50)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 0, 10, 0)
        main_layout.setSpacing(20)

        # Panel Izquierdo
        left_panel = QHBoxLayout()
        left_panel.setSpacing(10)

        btn_camera = QPushButton("📷")
        btn_camera.setFixedSize(30, 30)
        left_panel.addWidget(btn_camera)

        combo_camera = QComboBox()
        combo_camera.setFixedSize(100, 30)
        combo_camera.addItems(["-", "Cámara 1", "Cámara 2"])
        left_panel.addWidget(combo_camera)

        btn_refresh = QPushButton("🔁")
        btn_refresh.setFixedSize(30, 30)
        left_panel.addWidget(btn_refresh)

        # Panel Derecho
        right_panel = QHBoxLayout()
        right_panel.setSpacing(10)
        right_panel.setAlignment(Qt.AlignRight)

        combo_quality = QComboBox()
        combo_quality.setFixedSize(80, 30)
        combo_quality.addItems(["Original", "HD", "SD"])
        right_panel.addWidget(combo_quality)

        # Botón de vista 2x2
        right_panel.addWidget(self._crear_boton_grilla(2, 2, "Vista 4 cámaras", lambda: self.parent_liveview.set_layout(2, 2)))
        # Botón de vista 3x3
        right_panel.addWidget(self._crear_boton_grilla(3, 3, "Vista 9 cámaras", lambda: self.parent_liveview.set_layout(3, 3)))
        # Botón de vista 4x4
        right_panel.addWidget(self._crear_boton_grilla(4, 4, "Vista 16 cámaras", lambda: self.parent_liveview.set_layout(4, 4)))

        # Contenedores visuales
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        left_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        right_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)

    def _crear_boton_grilla(self, cols, rows, tooltip, callback):
        btn = QPushButton()
        btn.setToolTip(tooltip)
        btn.setFixedSize(30, 30)

        grid = QGridLayout()
        grid.setSpacing(1)
        grid.setContentsMargins(2, 2, 2, 2)

        for r in range(rows):
            for c in range(cols):
                cell = QLabel()
                cell.setFixedSize(6, 6)
                cell.setStyleSheet("background-color: white;")
                grid.addWidget(cell, r, c)

        container = QWidget()
        container.setLayout(grid)
        btn.setLayout(grid)
        btn.clicked.connect(callback)

        return btn
