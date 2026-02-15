from PySide6.QtGui import Qt, QPixmap
from PySide6.QtWidgets import QPushButton, QSizePolicy, QLabel

from core import Utility


class BaseButton(QPushButton):
    def __init__(self, path, styling, display_image_filename):
        super().__init__()
        self._path = path
        self._image_label = QLabel(self)
        self._styling = styling
        self._display_image_filename = display_image_filename

    def initialize(self):
        self._set_style()
        self._initialize_image_label()

    def _set_style(self):
        self.setStyleSheet(self._styling)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def _initialize_image_label(self):
        self._image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._image_label.setScaledContents(True)

        pixmap = QPixmap(Utility.get_image_path(self._display_image_filename, self._path))
        self._image_label.setPixmap(pixmap)

    def resizeEvent(self, event):
        self._image_label.setFixedSize(event.size()) #damit wird das Icon so groß wie der Button gesetzt
        super().resizeEvent(event)