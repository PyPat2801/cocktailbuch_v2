from PySide6.QtWidgets import QLineEdit, QSizePolicy
from PySide6.QtCore import Signal, Qt

from core import Rectangle, SheetLeftStyle, FontDivisors


class TypeTemplate(QLineEdit):

    def __init__(self, config: Rectangle, styling: SheetLeftStyle):
        super().__init__()
        self._config = config
        self._styling = styling

    def initialize(self):
        self._set_style()

    def _set_style(self):
        self.setStyleSheet(self._styling.drink_title)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setPlaceholderText("Typ eingeben …")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_size()

    def _update_font_size(self):
        profile = FontDivisors.get_active_font_profile_for_widget(self)
        divisor = profile["font_type"]
        font_size = int(self.width() / divisor)
        font_size = max(12, min(120, font_size))

        style = self._styling.drink_title.format(font_size=font_size)
        self.setStyleSheet(style)

    def get_value(self) -> str:
        return self.text().strip()
