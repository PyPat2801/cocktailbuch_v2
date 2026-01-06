from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class BaseTextLabel(QLabel):
    def __init__(self, text: str, styling: str):
        super().__init__()
        self._text = text
        self._styling = styling

    def initialize(self):
        self._set_style()

    def _set_style(self):
        home_text = self._text
        self.setText(home_text)
        self.setStyleSheet(self._styling)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
