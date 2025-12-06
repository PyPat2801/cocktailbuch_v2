from PySide6.QtGui import Qt, QPixmap
from PySide6.QtWidgets import QPushButton, QSizePolicy, QLabel
from core.utility import Utility


class GotoDrinksButton(QPushButton):
    def __init__(self, goto_drinks_callback):
        super().__init__()

        self._image_label = QLabel(self)
        self._callback = goto_drinks_callback

    def initialize(self):
        self._set_style()
        self._initialize_image_label()

    def _set_style(self):
        self.setStyleSheet("background-color: transparent; border: none;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def _initialize_image_label(self):
        self._image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._image_label.setScaledContents(True)

        pixmap = QPixmap(Utility.get_image_path("go_to_drinks.png", "icons"))
        self._image_label.setPixmap(pixmap)

        if self._callback:
            self.clicked.connect(self._callback)

    def resizeEvent(self, event):
        self._image_label.setFixedSize(event.size()) #damit wird das Icon so groß wie der Button gesetzt
        super().resizeEvent(event)




