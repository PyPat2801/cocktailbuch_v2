from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel
from core import FontDivisors, HomeTextStyle


class BaseTextLabel(QLabel):
    def __init__(self, text: str, font_size_type: str, styling: str = HomeTextStyle.text_style):
        super().__init__()
        self._text = text
        self._styling = styling
        self._font_size_type = font_size_type

    def initialize(self):
        self._set_style()

    def _set_style(self):
        home_text = self._text
        self.setText(home_text)
        self.setStyleSheet(self._styling)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_size()

    def _update_font_size(self):
        profile = FontDivisors.get_active_font_profile_for_widget(self)
        divisor = profile[self._font_size_type]
        font_size = int(self.width() / divisor)
        font_size = max(12, min(120, font_size))
        style = self._styling.format(font_size=font_size)
        self.setStyleSheet(style)
