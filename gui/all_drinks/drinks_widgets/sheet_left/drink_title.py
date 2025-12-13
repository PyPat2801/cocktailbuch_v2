from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from core import Rectangle, SheetLeftStyle


class DrinkTitle(QLabel):
    def __init__(self, config: Rectangle, styling: SheetLeftStyle):
        super().__init__()
        self._config = config
        self._styling = styling

    def initialize(self):
        self._set_style()

    def _set_style(self):
        self.setStyleSheet(self._styling.drink_title)
        self.setAlignment(Qt.AlignCenter)
        self.setWordWrap(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_size()

    def _update_font_size(self):
        font_size = int(min(self.width() * 0.5, self.width() / 7))
        font_size = max(12, font_size)
        font_size = min(120, font_size)

        style = self._styling.drink_title.format(font_size=font_size)
        self.setStyleSheet(style)
