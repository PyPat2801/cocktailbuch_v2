from PySide6.QtWidgets import QLabel

from core import Rectangle, SheetLeftStyle


class DrinkTitle(QLabel):
    def __init__(self, config: Rectangle, styling: SheetLeftStyle):
        super().__init__()
        self._config = config
        self._styling = styling

    def initialize(self):
        self._set_style()

    def _set_style(self):
        self.setStyleSheet(self._styling.drink_title)
