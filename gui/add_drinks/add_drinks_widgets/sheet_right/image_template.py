from typing import Optional

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QFileDialog

from core import Rectangle, SheetRightStyle, Utility


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

    def set_image_from_bytes(self, image_bytes: bytes) -> None:
        pixmap = QPixmap()
        if not pixmap.loadFromData(image_bytes):
            return

        self._original_pixmap = pixmap
        self._image_path = "__from_db__"  # Sentinel, damit image_ok in Validation True bleibt

        self.adjust_image_size()
        self._image.setText("")
        self.image_selected.emit(self._image_path)

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
        cropped = Utility.scale_and_crop_center(
            self._original_pixmap,
            target_size
        )
        self._image.setPixmap(cropped)
        self._image.setScaledContents(False)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_image_size()

    def get_value(self) -> str:
        pass

    def set_value(self, value: str) -> None:
        pass


