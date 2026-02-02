from PySide6.QtWidgets import QPushButton, QSizePolicy

from core import ArrowBarStyle


class ArrowBar(QPushButton):
    def __init__(self, label, styling: ArrowBarStyle):
        super().__init__(label)
        self._styling = styling

    def initialize(self):
        self.setStyleSheet(self._styling.background)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
