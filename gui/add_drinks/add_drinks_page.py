from PySide6.QtWidgets import QWidget
from gui.add_drinks.add_drinks_widgets import GotoHomeButton
from core import AddDrinksConfig, DataBase, AddDrinksStyle


class AddDrinksPage(QWidget):
    def __init__(self, configuration: AddDrinksConfig, styling: AddDrinksStyle, path: str, goto_home_callback, database: DataBase):
        super().__init__()

        self._config = configuration
        self._styling = styling
        self._database = database

        self._goto_home_button = GotoHomeButton(path, goto_home_callback)

    def initialize(self, layout):
        self._goto_home_button.initialize()
        self._add_goto_home_button(layout)
        self.setLayout(layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def _add_goto_home_button(self, layout):
        layout.addWidget(
            self._goto_home_button,
            self._config.goto_home_button.origin_y,
            self._config.goto_home_button.origin_x,
            self._config.goto_home_button.height,
            self._config.goto_home_button.width,
        )
