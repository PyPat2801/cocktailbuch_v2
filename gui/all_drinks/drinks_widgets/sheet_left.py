from PySide6.QtWidgets import QLabel


class SheetLeft(QLabel):
    def __init__(self, config):
        super().__init__()
        self._config = config

    def initialize(self):
        self._set_style()

    def _set_style(self):
        self.setStyleSheet("""
            QLabel {
                background-color: red;border: 1px solid black;
            }""")

