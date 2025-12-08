from PySide6.QtWidgets import QWidget

from core import DataBase, AllDrinksConfig, AllDrinksStyle
from gui.all_drinks.drinks_widgets import GotoHomeButton, SheetRight, ArrowBar
from gui.all_drinks.drinks_widgets.sheet_left import DrinkTitle, DrinkIngredients, DrinkDescription, DrinkType


class AllDrinksPage(QWidget):
    def __init__(self, configuration: AllDrinksConfig, styling: AllDrinksStyle,  path: str, goto_home_callback, database: DataBase):
        super().__init__()

        self._config = configuration
        self._styling = styling
        self._database = database
        self._goto_home_button = GotoHomeButton(path, goto_home_callback)

        self._arrow_left = ArrowBar("<=", lambda: True, styling.arrow_style)

        self._drink_title = DrinkTitle(configuration.drink_title, styling.sheet_left_style)
        self._drink_ingredients = DrinkIngredients(configuration.drink_ingredients, styling.sheet_left_style)
        self._drink_description = DrinkDescription(configuration.drink_description, styling.sheet_left_style)
        self._drink_type = DrinkType(configuration.drink_type, styling.sheet_left_style)

        self._sheet_right = SheetRight(configuration.sheet_right)

    def initialize(self, layout):
        self._goto_home_button.initialize()
        self._arrow_left.initialize()

        self._drink_title.initialize()
        self._drink_ingredients.initialize()
        self._drink_description.initialize()
        self._drink_type.initialize()

        self._sheet_right.initialize()

        self._add_goto_home_button(layout)
        self._add_arrow_left(layout)

        self._add_drink_title(layout)
        self._add_drink_ingredients(layout)
        self._add_drink_description(layout)
        self._add_drink_type(layout)

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

    def _add_drink_title(self, layout):
        layout.addWidget(
            self._drink_title,
            self._config.drink_title.origin_y,
            self._config.drink_title.origin_x,
            self._config.drink_title.height,
            self._config.drink_title.width,
        )

    def _add_drink_ingredients(self, layout):
        layout.addWidget(
            self._drink_ingredients,
            self._config.drink_ingredients.origin_y,
            self._config.drink_ingredients.origin_x,
            self._config.drink_ingredients.height,
            self._config.drink_ingredients.width,
        )

    def _add_drink_description(self, layout):
        layout.addWidget(
            self._drink_description,
            self._config.drink_description.origin_y,
            self._config.drink_description.origin_x,
            self._config.drink_description.height,
            self._config.drink_description.width,
        )

    def _add_drink_type(self, layout):
        layout.addWidget(
            self._drink_type,
            self._config.drink_type.origin_y,
            self._config.drink_type.origin_x,
            self._config.drink_type.height,
            self._config.drink_type.width,
        )

    def _add_sheet_right(self, layout):
        layout.addWidget(
            self._sheet_right,
            self._config.sheet_right.origin_y,
            self._config.sheet_right.origin_x,
            self._config.sheet_right.height,
            self._config.sheet_right.width,
        )

