from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFontMetrics, QFont

from core import Rectangle, FontDivisors, SheetLeftStyle
from PySide6.QtWidgets import QLineEdit, QSizePolicy


class TitleTemplate(QLineEdit):

    def __init__(self, config: Rectangle, styling: SheetLeftStyle):
        super().__init__()
        self._config = config
        self._styling = styling

    def initialize(self):
        self._set_style()
        self._update_font_size()

        self.textChanged.connect(self._update_font_size)

    def _set_style(self):
        self.setStyleSheet(self._styling.drink_title)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setPlaceholderText("Titel eingeben …")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_size()

    def _update_font_size(self):
        text = (self.text() or "").strip()

        widget_width = max(1, self.contentsRect().width())

        profile = FontDivisors.get_active_font_profile_for_widget(self)
        divisor = profile["font_title"]
        font_size = int(widget_width / divisor)
        font_size = max(12, min(120, font_size))

        # Falls Text nicht in widget_width passt, dann reduziere ihn
        if text:
            reserve = 5
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

    def get_value(self) -> str:
        return self.text().strip()


