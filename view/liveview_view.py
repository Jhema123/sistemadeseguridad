from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QLabel, QGridLayout
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from view.toolbar_view import ToolbarView

class LiveView(QWidget):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.camera_widgets = {}
        self.setWindowTitle("Live View")
        self.setStyleSheet("background-color: #1E1E1E; color: white;")
        self.init_ui()



    def set_controller(self, controller):
        self.controller = controller

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        sidebar = QVBoxLayout()

        label = QLabel("Organización")
        label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        sidebar.addWidget(label)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemDoubleClicked.connect(self.on_camera_selected)
        sidebar.addWidget(self.tree)

        right_panel = QVBoxLayout()

        self.grid = QGridLayout()
        self.set_layout(2, 2)

        right_panel.addLayout(self.grid)

        # ✅ Toolbar en la parte inferior de la grilla
        toolbar = ToolbarView(self)
        right_panel.addWidget(toolbar)

        # Estructura final: [sidebar | right_panel]
        main_layout.addLayout(sidebar, 1)
        main_layout.addLayout(right_panel, 4)

        self.setLayout(main_layout)

    def populate_camera_tree(self, camera_indexes):
        self.tree.clear()
        root = QTreeWidgetItem(["Ver"])
        self.tree.addTopLevelItem(root)
        for idx in camera_indexes:
            QTreeWidgetItem(root, [f"Cámara {idx}"])
        self.tree.expandAll()

    def set_layout(self, rows, cols):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.camera_widgets.clear()
        count = 0
        for r in range(rows):
            for c in range(cols):
                label = QLabel()
                label.setMinimumSize(QSize(160, 120))
                label.setStyleSheet("background-color: black; border: 1px solid gray;")
                label.setScaledContents(True)
                self.grid.addWidget(label, r, c)
                self.camera_widgets[count] = label
                count += 1

    def on_camera_selected(self, item, _):
        if not self.controller:
            return
        if "Cámara" in item.text(0):
            index = int(item.text(0).split()[-1])
            for label in self.camera_widgets.values():
                if label.pixmap() is None:
                    self.controller.assign_camera(index, label)
                    break
