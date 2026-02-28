from typing import Optional

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QSize

from core import Utility


class DrinkImage(QLabel):
    def __init__(self, database):
        super().__init__()
        self._database = database
        self.drink_image = QLabel(self)
        self._layout = QVBoxLayout()

        self._original_pixmap: Optional[QPixmap] = None

    def initialize(self):
        self.initialize_image()

    def initialize_image(self):
        self.drink_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._layout)
        self.layout().addWidget(self.drink_image)

    def _set_image(self, image_data: bytes):
        pixmap = QPixmap()
        if not pixmap.loadFromData(image_data):
            return

        self._original_pixmap = pixmap
        self._adjust_image_size()

    def update_image(self, image_data):
        self._set_image(image_data)

    def _adjust_image_size(self, width: Optional[int] = None, height: Optional[int] = None) -> None:
        if self._original_pixmap is None or self._original_pixmap.isNull():
            return

        if width is None or height is None:
            width = self.drink_image.width()
            height = self.drink_image.height()
        if width <= 0 or height <= 0:
            return

        target_size = QSize(width, height)

        cropped = Utility.scale_and_crop_center(
            self._original_pixmap,
            target_size
        )

        self.setPixmap(cropped)
        self.setScaledContents(False)

    def clear_image(self) -> None:
        self._original_pixmap = None
        self.drink_image.clear()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._adjust_image_size()

