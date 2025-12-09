from PySide6.QtWidgets import QWidget

from core import DataBase, HomePageConfig, HomeStyle
from gui.home.home_widgets import GotoDrinksButton, HomeIcon, AddDrinksButton, FindDrinksButton, HomeText


class HomePage(QWidget):
    def __init__(self, configuration: HomePageConfig, styling: HomeStyle, path: str, goto_drinks_callback, database : DataBase):
        super().__init__()
        self._config = configuration
        self._database = database
        self._styling = styling
        self.home_icon = HomeIcon(path)
        self.home_text = HomeText(styling.text_style)
        self.goto_drinks_button = GotoDrinksButton(path, goto_drinks_callback)
        self.add_drinks_button = AddDrinksButton(path)
        self.find_drinks_button = FindDrinksButton(path)

    def initialize(self, layout):
        self.home_icon.initialize()
        self.home_text.initialize()
        self.goto_drinks_button.initialize()
        self.add_drinks_button.initialize()
        self.find_drinks_button.initialize()

        self._add_home_icon(layout)
        self._add_home_text(layout)
        self._add_goto_drinks_button(layout)
        self._add_add_drinks_button(layout)
        self._add_find_drinks_button(layout)
        self.setLayout(layout)

    def resizeEvent(self, event):
        """Handle resize events by updating icon size based on new grid dimensions."""
        # Rufe die Parent-Implementierung auf
        super().resizeEvent(event)

    def _add_home_icon(self, layout):
        layout.addWidget(
                self.home_icon,
                self._config.home_icon.origin_y,  # row
                self._config.home_icon.origin_x,  # column
                self._config.home_icon.height,  # rowSpan
                self._config.home_icon.width  # columnSpan
        )

    def _add_goto_drinks_button(self, layout):
        layout.addWidget(
                self.goto_drinks_button,
                self._config.goto_drinks_button.origin_y,
                self._config.goto_drinks_button.origin_x,
                self._config.goto_drinks_button.height,
                self._config.goto_drinks_button.width,
        )

    def _add_add_drinks_button(self, layout):
        layout.addWidget(
            self.add_drinks_button,
            self._config.add_drinks_button.origin_y,
            self._config.add_drinks_button.origin_x,
            self._config.add_drinks_button.height,
            self._config.add_drinks_button.width,
        )

    def _add_find_drinks_button(self, layout):
        layout.addWidget(
            self.find_drinks_button,
            self._config.find_drinks_button.origin_y,
            self._config.find_drinks_button.origin_x,
            self._config.find_drinks_button.height,
            self._config.find_drinks_button.width,
        )

    def _add_home_text(self, layout):
        layout.addWidget(
            self.home_text,
            self._config.home_text.origin_y,
            self._config.home_text.origin_x,
            self._config.home_text.height,
            self._config.home_text.width,
        )
