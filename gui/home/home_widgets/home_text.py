from PySide6.QtWidgets import QLabel
from PySide6.QtGui import Qt, QFont


class HomeText(QLabel):
    def __init__(self):
        super().__init__()

    def initialize(self):
        self._set_style()

    def _set_style(self):
        home_text = "Miri's und Patrick's Cocktailbuch"
        self.setText(home_text)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.setStyleSheet("""
            color: white;
            font-size: 48px;
            font-family: "Brush Script MT", "Segoe Script", "Cursive", "sans-serif";
            background-color: red;
        """)
        self.setWordWrap(True)

    def resizeEvent(self, event):
        self._update_font()
        super().resizeEvent(event)

    def _update_font(self):
        height = self.height()
        width = self.width()
        font_size = max(8, min(height // 4, width // 18))
        font = QFont("Brush Script MT")
        font.setPointSize(font_size)
        self.setFont(font)

