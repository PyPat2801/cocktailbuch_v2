from PySide6.QtWidgets import QWidget

from core import DataBase, AllDrinksConfig, AllDrinksStyle
from gui.all_drinks.drinks_widgets import GotoHomeButton, SheetLeft, SheetRight, ArrowBar


class AllDrinksPage(QWidget):
    def __init__(self, configuration: AllDrinksConfig, styling: AllDrinksStyle, goto_home_callback, database: DataBase):
        super().__init__()

        self._config = configuration
        self._styling = styling
        self._database = database
        self._goto_home_button = GotoHomeButton(goto_home_callback)
        self._arrow_left = ArrowBar("<=", lambda: True, styling.arrow_style)
        self._sheet_left = SheetLeft(configuration.sheet_left, styling.sheet_left_style)
        self._sheet_right = SheetRight(configuration.sheet_right)

    def initialize(self, layout):
        self._goto_home_button.initialize()
        self._arrow_left.initialize()
        self._sheet_left.initialize()
        self._sheet_right.initialize()

        self._add_goto_home_button(layout)
        self._add_arrow_left(layout)
        self._add_sheet_left(layout)
        self._add_sheet_right(layout)

        self.setLayout(layout)
        self._goto_home_button.raise_() # overlaps the other widgets
        self._arrow_left.raise_() # overlaps the other widgets

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
    
    def _add_arrow_left(self, layout):
        layout.addWidget(
            self._arrow_left,
            self._config.arrow_left.origin_y,
            self._config.arrow_left.origin_x,
            self._config.arrow_left.height,
            self._config.arrow_left.width
        )

    def _add_sheet_left(self, layout):
        layout.addWidget(
            self._sheet_left,
            self._config.sheet_left.origin_y,
            self._config.sheet_left.origin_x,
            self._config.sheet_left.height,
            self._config.sheet_left.width,
        )

    def _add_sheet_right(self, layout):
        layout.addWidget(
            self._sheet_right,
            self._config.sheet_right.origin_y,
            self._config.sheet_right.origin_x,
            self._config.sheet_right.height,
            self._config.sheet_right.width,
        )

