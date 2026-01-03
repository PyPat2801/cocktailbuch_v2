
from PySide6.QtWidgets import QPushButton

from core import Rectangle, SheetRightStyle


class ConfirmDrinkButton(QPushButton):
    def __init__(self, config: Rectangle, styling: SheetRightStyle):
        super().__init__()
        self._config = config
        self._styling = styling

    def initialize(self):
        self.setText("Confirm")
        self.setStyleSheet(self._styling.confirm_button)
