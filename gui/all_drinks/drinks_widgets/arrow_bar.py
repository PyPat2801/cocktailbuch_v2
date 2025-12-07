from PySide6.QtWidgets import QPushButton

from core import ArrowBarStyle


class ArrowBar(QPushButton):
    def __init__(self, label, callback, styling: ArrowBarStyle):
        super().__init__(label)

        self.callback = callback
        self._styling = styling

        self.clicked.connect(self.on_click)

    def initialize(self):
        self.setStyleSheet(self._styling.background) 

    def on_click(self) -> None:
        self.callback()