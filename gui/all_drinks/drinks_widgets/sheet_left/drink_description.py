from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from core import Rectangle, SheetLeftStyle, FontDivisors


class DrinkDescription(QLabel):
    def __init__(self, config: Rectangle, styling: SheetLeftStyle):
        super().__init__()
        self._config = config
        self._styling = styling

    def initialize(self):
        self._set_style()

    def _set_style(self):
        self.setStyleSheet(self._styling.drink_description)
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setWordWrap(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_size()

    def _update_font_size(self):
        profile = FontDivisors.get_active_font_profile_for_widget(self)
        divisor = profile["font_description"]
        font_size = int(self.width() / divisor)
        font_size = max(12, min(120, font_size))

        style = self._styling.drink_description.format(font_size=font_size)
        self.setStyleSheet(style)
