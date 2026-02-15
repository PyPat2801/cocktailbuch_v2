from PySide6.QtWidgets import QLineEdit, QSizePolicy
from core import SearchInputStyle, FontDivisors
from PySide6.QtGui import QFontMetrics, QFont


class SearchInput(QLineEdit):
    def __init__(self, styling: SearchInputStyle):
        super().__init__()

        self._styling = styling

    def initialize(self):
        self._set_style()
        self._update_font_size()

    def _set_style(self):
        self.setStyleSheet(self._styling.input_style)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setPlaceholderText("Hier was auch immer eingeben...")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_size()

    def _update_font_size(self):
        text = (self.text() or "").strip()

        widget_width = max(1, self.contentsRect().width())

        profile = FontDivisors.get_active_font_profile_for_widget(self)
        divisor = profile["font_search_by_input"]
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

        style = self._styling.input_style.format(font_size=font_size)
        self.setStyleSheet(style)
