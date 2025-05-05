from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QLabel, QPushButton,
    QListWidget, QGridLayout, QDateEdit, QTimeEdit, QRadioButton, QSlider
)
from PyQt5.QtCore import Qt, QDate, QTime, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl


class RecordingView(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1E1E1E; color: white;")
        self.controller = None
        self.video_widgets = []
        self.reproductores = []  # (player, widget)
        self.reproductor_activo = None
        self.video_expandidos = {}
        self.velocidades = [0.25, 0.5, 1.0, 1.5, 2.0]
        self.velocidad_index = 2  # corresponde a 1X

        self.init_ui()

    def set_controller(self, controller):
        self.controller = controller

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # Sidebar
        sidebar = QVBoxLayout()
        title = QLabel("Grabaciones")
        title.setFont(QFont("Segoe UI", 10, QFont.Bold))
        sidebar.addWidget(title)

        self.camera_tree = QTreeWidget()
        self.camera_tree.setHeaderHidden(True)
        sidebar.addWidget(self.camera_tree)

        sidebar.addWidget(QLabel("Ver:"))
        self.radio_record = QRadioButton("Record")
        self.radio_record.setChecked(True)
        self.radio_picture = QRadioButton("Picture")
        self.radio_fecha_exacta = QRadioButton("Solo Fecha")
        self.radio_rango = QRadioButton("Fecha + Hora")
        self.radio_rango.setChecked(True)
        sidebar.addWidget(self.radio_record)
        sidebar.addWidget(self.radio_picture)
        sidebar.addWidget(self.radio_fecha_exacta)
        sidebar.addWidget(self.radio_rango)

        sidebar.addWidget(QLabel("Inicio"))
        start_layout = QHBoxLayout()
        self.start_date = QDateEdit(QDate.currentDate())
        self.start_time = QTimeEdit(QTime(0, 0, 0))
        start_layout.addWidget(self.start_date)
        start_layout.addWidget(self.start_time)
        sidebar.addLayout(start_layout)

        sidebar.addWidget(QLabel("Final"))
        end_layout = QHBoxLayout()
        self.end_date = QDateEdit(QDate.currentDate())
        self.end_time = QTimeEdit(QTime(23, 59, 59))
        end_layout.addWidget(self.end_date)
        end_layout.addWidget(self.end_time)
        sidebar.addLayout(end_layout)

        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.setStyleSheet("background-color: #00A8F3; color: white;")
        sidebar.addWidget(self.btn_buscar)

        self.lista_grabaciones = QListWidget()
        self.lista_grabaciones.setFixedHeight(160)
        sidebar.addWidget(self.lista_grabaciones)

        # Right panel
        right_panel = QVBoxLayout()

        # Grid de reproducción
        self.grid = QGridLayout()
        self.set_layout(2, 2)
        right_panel.addLayout(self.grid)

        # Slider de tiempo
        slider_layout = QHBoxLayout()
        self.timeline_slider = QSlider(Qt.Horizontal)
        self.timeline_slider.setMinimum(0)
        self.timeline_slider.setMaximum(100)

        self.label_tiempo = QLabel("00:00 / 00:00")
        self.label_tiempo.setFixedWidth(90)
        self.label_tiempo.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        slider_layout.addWidget(self.timeline_slider)
        slider_layout.addWidget(self.label_tiempo)
        right_panel.addLayout(slider_layout)

        controls = QHBoxLayout()
        self.btn_rewind = QPushButton("⏪")
        self.btn_play = QPushButton("▶")
        self.btn_pause = QPushButton("⏸")
        self.btn_stop = QPushButton("⏹")
        self.btn_forward = QPushButton("⏩")
        self.velocidad_label = QLabel("1X")
        self.btn_mute = QPushButton("🔊")

        for btn in [self.btn_rewind, self.btn_play, self.btn_pause, self.btn_stop, self.btn_forward, self.velocidad_label, self.btn_mute]:
            btn.setFixedSize(36, 36)
            controls.addWidget(btn)

        controls.addStretch()

        self.btn_grid_2x2 = QPushButton("2x2")
        self.btn_grid_3x3 = QPushButton("3x3")
        self.btn_grid_4x4 = QPushButton("4x4")
        self.btn_expandir = QPushButton("⟳")

        for btn in [self.btn_grid_2x2, self.btn_grid_3x3, self.btn_grid_4x4, self.btn_expandir]:
            btn.setFixedSize(36, 36)
            controls.addWidget(btn)

        right_panel.addLayout(controls)

        self.btn_grid_2x2.clicked.connect(lambda: self.set_layout(2, 2))
        self.btn_grid_3x3.clicked.connect(lambda: self.set_layout(3, 3))
        self.btn_grid_4x4.clicked.connect(lambda: self.set_layout(4, 4))

        self.btn_play.clicked.connect(lambda: self.reproductor_activo.play() if self.reproductor_activo else None)
        self.btn_pause.clicked.connect(lambda: self.reproductor_activo.pause() if self.reproductor_activo else None)
        self.btn_stop.clicked.connect(lambda: self.reproductor_activo.stop() if self.reproductor_activo else None)

        self.btn_rewind.clicked.connect(self.disminuir_velocidad)
        self.btn_forward.clicked.connect(self.aumentar_velocidad)

        main_layout.addLayout(sidebar, 1)
        main_layout.addLayout(right_panel, 3)
        self.setLayout(main_layout)

        self.lista_grabaciones.itemDoubleClicked.connect(self.reproducir_en_celda)

    def set_layout(self, rows, cols):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.video_widgets = []
        self.reproductores = []
        for r in range(rows):
            for c in range(cols):
                widget = QVideoWidget()
                widget.setMinimumSize(QSize(160, 120))
                self.grid.addWidget(widget, r, c)
                self.video_widgets.append(widget)

                player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
                player.setVideoOutput(widget)
                self.reproductores.append((player, widget))

                widget.mouseDoubleClickEvent = lambda event, w=widget: self.expandir_video(w)

        if self.controller:
            self.controller.recrear_reproductores(self.video_widgets)

    def expandir_video(self, widget):
        if widget not in self.video_expandidos:
            self.video_expandidos[widget] = self.grid.indexOf(widget)
            for w in self.video_widgets:
                if w != widget:
                    w.hide()
            for i in reversed(range(self.grid.count())):
                self.grid.itemAt(i).widget().setParent(None)
            self.grid.addWidget(widget, 0, 0, 1, 1)
            widget.setMinimumSize(640, 480)
            for player, w in self.reproductores:
                if w == widget:
                    self.reproductor_activo = player
                    self.conectar_slider_a_reproductor(player)
                    break
        else:
            self.set_layout(2, 2)
            self.video_expandidos.pop(widget)
            self.reproductor_activo = None

    def conectar_slider_a_reproductor(self, player):
        try:
            player.positionChanged.disconnect()
            player.durationChanged.disconnect()
            self.timeline_slider.sliderMoved.disconnect()
        except:
            pass

        def actualizar_tiempo(position):
            duracion = player.duration()
            tiempo_actual = self.formatear_tiempo(position)
            tiempo_total = self.formatear_tiempo(duracion)
            self.label_tiempo.setText(f"{tiempo_actual} / {tiempo_total}")
            self.timeline_slider.setValue(position)

        def actualizar_duracion(duration):
            self.timeline_slider.setMaximum(duration)
            tiempo_total = self.formatear_tiempo(duration)
            tiempo_actual = self.formatear_tiempo(player.position())
            self.label_tiempo.setText(f"{tiempo_actual} / {tiempo_total}")

        player.positionChanged.connect(actualizar_tiempo)
        player.durationChanged.connect(actualizar_duracion)
        self.timeline_slider.sliderMoved.connect(player.setPosition)

    def formatear_tiempo(self, ms):
        segundos = int(ms / 1000)
        minutos = int(segundos / 60)
        segundos = int(segundos % 60)
        return f"{minutos:02}:{segundos:02}"

    def reproducir_en_celda(self, item):
        ruta = item.text().split(" - ")[-1].strip()
        for player, _ in self.reproductores:
            if player.mediaStatus() != QMediaPlayer.LoadedMedia and player.mediaStatus() != QMediaPlayer.BufferedMedia:
                player.setMedia(QMediaContent(QUrl.fromLocalFile(ruta)))
                player.play()
                break

    def aumentar_velocidad(self):
        if not self.reproductor_activo:
            return
        if self.velocidad_index < len(self.velocidades) - 1:
            self.velocidad_index += 1
            nueva = self.velocidades[self.velocidad_index]
            self.reproductor_activo.setPlaybackRate(nueva)
            self.velocidad_label.setText(f"{nueva}X")

    def disminuir_velocidad(self):
        if not self.reproductor_activo:
            return
        if self.velocidad_index > 0:
            self.velocidad_index -= 1
            nueva = self.velocidades[self.velocidad_index]
            self.reproductor_activo.setPlaybackRate(nueva)
            self.velocidad_label.setText(f"{nueva}X")
