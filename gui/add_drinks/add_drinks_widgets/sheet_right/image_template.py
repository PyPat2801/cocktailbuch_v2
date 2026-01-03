from typing import Optional

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QFileDialog

from core import Rectangle, SheetRightStyle


class ImageTemplate(QLabel):

    image_selected = Signal(str)

    def __init__(self, config: Rectangle, styling: SheetRightStyle):
        super().__init__()
        self._config = config
        self._styling = styling

        self._image = QLabel(self)
        self._layout = QVBoxLayout()

        self._original_pixmap: Optional[QPixmap] = None
        self._image_path: Optional[str] = None

    def initialize(self):
        self._initialize_image_widget_and_style()

    def _initialize_image_widget_and_style(self):
        self._image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.layout().addWidget(self._image)

        self._image.setText("Klick: Bild auswählen")
        self._image.setStyleSheet(self._styling.drink_image)

    def get_image_path(self) -> Optional[str]:
        return self._image_path

    def clear(self) -> None:
        self._image_path = None
        self._original_pixmap = None

        self._image.clear()
        self._image.setText("Klick: Bild auswählen")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._open_file_dialog()
        super().mousePressEvent(event)

    def _open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Bild auswählen",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)"
        )
        if not path:
            return

        pixmap = QPixmap(path)
        if pixmap.isNull():
            return

        self._image_path = path
        self._original_pixmap = pixmap

        self.adjust_image_size()
        self._image.setText("")
        self.image_selected.emit(path)

    def adjust_image_size(self, width: Optional[int] = None, height: Optional[int] = None):
        if self._original_pixmap is None:
            return

        if width is None or height is None:
            width = self._image.width()
            height = self._image.height()

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

        self._image.setPixmap(image_cropped)
        self._image.setScaledContents(False)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_image_size()
