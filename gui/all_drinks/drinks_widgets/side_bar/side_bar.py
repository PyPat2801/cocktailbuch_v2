from PySide6.QtWidgets import QLabel


class SideBar(QLabel):
    def __init__(self, styling):
        super().__init__()
        self._styling = styling

    def initialize(self):
        self._set_style()

    def _set_style(self):
        self.setStyleSheet(self._styling.background)

