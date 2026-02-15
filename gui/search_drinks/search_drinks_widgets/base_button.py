from PySide6.QtGui import Qt, QPixmap
from PySide6.QtWidgets import QPushButton, QLabel, QSizePolicy

from core import Utility


class BaseButton(QPushButton):
    def __init__(self, path, styling, image_names):
        super().__init__()

        self._path = path
        self._image_label = QLabel(self)
        self._styling = styling.buttons_style
        self._display_image_filename = image_names

    def initialize(self):
        self._set_style()
        self._initialize_image_label()

    def _set_style(self):
        self.setStyleSheet(self._styling)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def _initialize_image_label(self):
        self._image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._image_label.setScaledContents(True)

        pixmap = QPixmap(Utility.get_image_path(self._display_image_filename, self._path))
        self._image_label.setPixmap(pixmap)

    def resizeEvent(self, event):
        self._image_label.setFixedSize(event.size())
        super().resizeEvent(event)