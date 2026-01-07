from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import QLabel, QSizePolicy

from core import SheetLeftStyle, FontDivisors


class DrinkTitle(QLabel):
    def __init__(self, styling: SheetLeftStyle):
        super().__init__()
        self._styling = styling

    def initialize(self):
        self._set_style()
        self._update_font_size()

    def _set_style(self):
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)
        self.setMinimumHeight(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_size()

    def set_text(self, text: str):
        self.setText(text)
        self._update_font_size()

    def _update_font_size(self):
        text = (self.text() or "").strip()

        # Berechnung der default Schriftgröße. Hier wird noch nicht berücksichtigt,
        # dass ein nötiger Zeilenumbruch vorliegt und daher die fontsize reduziert werden muss.
        # Das wird auch im resizeEvent getriggert
        widget_width = max(1, self.contentsRect().width())
        profile = FontDivisors.get_active_font_profile_for_widget(self)
        divisor = profile["font_title"]
        font_size = int(widget_width / divisor)
        font_size = max(12, min(120, font_size))

        # Falls Text nicht in widget_width_passt, dann reduziere ihn
        if text:
            reserve = 5  # verhindere Kanteneffekte
            target_width = max(1, widget_width - reserve)

            f = QFont(self.font())
            while font_size > 12:
                f.setPointSize(font_size)
                fm = QFontMetrics(f)

                if fm.horizontalAdvance(text) <= target_width:
                    break
                font_size -= 1

        style = self._styling.drink_title.format(font_size=font_size)
        self.setStyleSheet(style)
