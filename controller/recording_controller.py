from PyQt5.QtCore import QDate, QTime
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from datetime import datetime
from model.grabacion_model import GrabacionesModel
from view.recording_view import RecordingView
from PyQt5.QtWidgets import QTreeWidgetItem


class RecordingController:
    def __init__(self):
        self.model = GrabacionesModel()
        self.view = RecordingView()
        self.view.set_controller(self)
        self.media_players = []
        self.camara_seleccionada = 0

        self.view.btn_buscar.clicked.connect(self.buscar_grabaciones)
        self.cargar_camaras_en_arbol()

    def mostrar(self):
        return self.view

    def cargar_camaras_en_arbol(self):
        import cv2
        self.view.camera_tree.clear()
        root = QTreeWidgetItem(["Cámaras disponibles"])
        self.view.camera_tree.addTopLevelItem(root)
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                QTreeWidgetItem(root, [f"Cámara {i}"])
                cap.release()
        self.view.camera_tree.expandAll()
        self.view.camera_tree.itemClicked.connect(self.on_camera_selected)

    def on_camera_selected(self, item, _):
        if "Cámara" in item.text(0):
            self.camara_seleccionada = int(item.text(0).split()[-1])

    def buscar_grabaciones(self):
        camara = self.camara_seleccionada
        self.view.lista_grabaciones.clear()

        # ✅ Obtener fechas
        fecha_ini = self.view.start_date.date().toPyDate()
        hora_ini = self.view.start_time.time().toPyTime()
        fecha_fin = self.view.end_date.date().toPyDate()
        hora_fin = self.view.end_time.time().toPyTime()

        # ✅ Lógica según tipo de búsqueda
        if self.view.radio_fecha_exacta.isChecked():
            grabaciones = self.model.obtener_grabaciones_por_camara_y_fecha_exacta(camara, fecha_ini)
        else:
            inicio = datetime.combine(fecha_ini, hora_ini)
            fin = datetime.combine(fecha_fin, hora_fin)
            grabaciones = self.model.obtener_grabaciones_por_camara_y_rango(camara, inicio, fin)

        for g in grabaciones:
            texto = f"{g['inicio'].strftime('%Y-%m-%d %H:%M:%S')} - {g['ruta']}"
            self.view.lista_grabaciones.addItem(texto)

    def recrear_reproductores(self, video_widgets):
        self.media_players = []
        for widget in video_widgets:
            player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
            player.setVideoOutput(widget)
            self.media_players.append(player)

    def reproducir_en_primera_celda_libre(self, texto):
        # Extrae la ruta desde el texto del QListWidget
        ruta = texto.split(" - ")[-1].strip()
        for player in self.media_players:
            if player.mediaStatus() != QMediaPlayer.LoadedMedia and player.mediaStatus() != QMediaPlayer.BufferedMedia:
                player.setMedia(QMediaContent(QUrl.fromLocalFile(ruta)))
                player.play()
                break
