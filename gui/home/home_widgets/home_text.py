from PySide6.QtWidgets import QLabel
from PySide6.QtGui import Qt


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
            font-family: "Brush Script MT", "Segoe Script", "Cursive", "sans-serif";
            background-color: red;
        """)
        self.setWordWrap(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_size()

    def _update_font_size(self):

        font_size = int(min(self.width() * 0.5, self.width() / 9))
        font_size = max(12, font_size)
        font_size = min(120, font_size)

        self.setStyleSheet(f"""
            color: white;
            background-color: transparent;
            font-size: {font_size}px;
            font-family: "Brush Script MT", "Segoe Script", "Cursive", "sans-serif";
        """)


