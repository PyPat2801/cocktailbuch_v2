from PySide6.QtGui import Qt, QPixmap
from PySide6.QtWidgets import QPushButton, QLabel, QSizePolicy
from core import Utility


class DrinkDelete(QPushButton):
    def __init__(self, path, delete_callback=None):
        super().__init__()
        self._path = path
        self._image_label = QLabel(self)
        self._callback = delete_callback

    def initialize(self):
        self._set_style()
        self._initialize_image_label()

        if callable(self._callback):
            self.clicked.connect(self._callback)

    def _set_style(self):
        self.setStyleSheet("background-color: transparent; border: None; ")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def _initialize_image_label(self):
        self._image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._image_label.setScaledContents(True)

        pixmap = QPixmap(Utility.get_image_path("delete_transparent.png", self._path))
        self._image_label.setPixmap(pixmap)

    def resizeEvent(self, event):
        self._image_label.setFixedSize(event.size())
        super().resizeEvent(event)
