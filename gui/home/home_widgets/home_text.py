from PySide6.QtWidgets import QLabel
from PySide6.QtGui import Qt
from core import HomeTextStyle, FontDivisors


class HomeText(QLabel):
    def __init__(self, styling: HomeTextStyle):
        super().__init__()
        self._styling = styling

    def initialize(self):
        self._set_style()

    def _set_style(self):
        home_text = "Miri's und Patrick's Cocktailbuch"
        self.setText(home_text)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.setStyleSheet(self._styling.text_style)
        self.setWordWrap(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_size()

    def _update_font_size(self):
        profile = FontDivisors.get_active_font_profile_for_widget(self)
        divisor = profile["font_home_text"]
        font_size = int(self.width() / divisor)
        font_size = max(12, min(120, font_size))

        style = self._styling.text_style.format(font_size=font_size)
        self.setStyleSheet(style)

