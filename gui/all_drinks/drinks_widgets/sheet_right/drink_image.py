from typing import Optional

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QSize


class DrinkImage(QLabel):
    def __init__(self, config, database):
        super().__init__()
        self._config = config
        self._database = database
        self._drink_image = QLabel(self)
        self._drink_image.setAlignment(Qt.AlignCenter)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self._drink_image)

        self._original_pixmap: Optional[QPixmap] = None

    def initialize(self):
        pass

    def _set_image(self, image_data: bytes):
        pixmap = QPixmap()
        if not pixmap.loadFromData(image_data):
            return

        self._original_pixmap = pixmap
        self.adjust_image_size()

    def update_image(self,image_data):
        self._set_image(image_data)

    def adjust_image_size(self, width: Optional[int] = None, height: Optional[int] = None):
        if self._original_pixmap is None:
            return

        if width is None or height is None:
            width = self._drink_image.width()
            height = self._drink_image.height()

        if width <= 0 or height <= 0:
            return

        target_size = QSize(width, height)

        original_size = self._original_pixmap.size()
        if original_size.width() <= 0 or original_size.height() <= 0:
            return

        original_aspect_ratio = original_size.width() / original_size.height()
        target_aspect_ratio = target_size.width() / target_size.height()

        if original_aspect_ratio > target_aspect_ratio:
            scaled_size = QSize(int(target_size.height() * original_aspect_ratio), target_size.height())
        else:
            scaled_size = QSize(target_size.width(), int(target_size.width() / original_aspect_ratio))

        scaled_pixmap = self._original_pixmap.scaled(scaled_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        size_diff = scaled_pixmap.size() - target_size

        x = int(0.5 * size_diff.width())
        y = int(0.5 * size_diff.height())

        image_cropped = scaled_pixmap.copy(x, y, target_size.width(), target_size.height())

        self._drink_image.setPixmap(image_cropped)
        self._drink_image.setScaledContents(False)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_image_size()

