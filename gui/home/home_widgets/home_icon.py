
from PySide6.QtWidgets import QLabel, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from core.utility import Utility


class HomeIcon(QLabel):

    def __init__(self, path) -> None:
        super().__init__()
        self._path = path
        self._label = QLabel(self)

        self._layout = QVBoxLayout(self)
        self._pixmap = QPixmap(Utility.get_image_path("logo_transparent.png", self._path))

    def initialize(self):
        self._set_style()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._label)
        self._initialize_image()

    def _set_style(self):
        self.setStyleSheet("background-color: transparent; border: none")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def _initialize_image(self):
        self._label.setAlignment(Qt.AlignCenter)
        self._label.setScaledContents(True)  # Bild wird einfach skaliert
        self._label.setPixmap(self._pixmap)

    def resizeEvent(self, event):
        self._label.setFixedSize(event.size()) # Bild immer so groß wie Button
        super().resizeEvent(event)

