from core import DataBase, AllDrinksConfig, AllDrinksStyle
from gui.all_drinks.drinks_widgets import ArrowBar
from gui.all_drinks.drinks_widgets.sheet_left import DrinkTitle, DrinkIngredients, DrinkDescription, DrinkType
from gui.all_drinks.drinks_widgets.sheet_right import DrinkImage

from gui.base_layer import BaseLayer


class AllDrinksPage(BaseLayer):
    def __init__(self, configuration: AllDrinksConfig, styling: AllDrinksStyle,  path: str, goto_home_callback, database: DataBase):
        super().__init__(configuration.goto_home_button, path, goto_home_callback)

        self._config = configuration
        self._styling = styling
        self._database = database

        self.current_cocktail_index = 0

        self._arrow_left = ArrowBar("<=", self.scroll_left, styling.arrow_style)
        self._arrow_right = ArrowBar("=>", self.scroll_right, styling.arrow_style)

        self._drink_title = DrinkTitle(configuration.drink_title, styling.sheet_left_style)
        self._drink_ingredients = DrinkIngredients(configuration.drink_ingredients, styling.sheet_left_style)
        self._drink_description = DrinkDescription(configuration.drink_description, styling.sheet_left_style)
        self._drink_type = DrinkType(configuration.drink_type, styling.sheet_left_style)

        self._drink_image = DrinkImage(configuration.drink_image, self._database)

    def initialize(self, layout):
        super().initialize(layout)

        self._initialize_home_page_widgets()
        self._add_home_page_widgets(layout)
        self.swap_pages()

    def _initialize_home_page_widgets(self):
        self._arrow_left.initialize()
        self._arrow_right.initialize()

        self._drink_title.initialize()
        self._drink_ingredients.initialize()
        self._drink_description.initialize()
        self._drink_type.initialize()

        self._drink_image.initialize()

    def _add_home_page_widgets(self, layout):
        self._add_arrow_left(layout)
        self._add_arrow_right(layout)

        self._add_drink_title(layout)
        self._add_drink_ingredients(layout)
        self._add_drink_description(layout)
        self._add_drink_type(layout)

        self._add_drink_image(layout)

        self.setLayout(layout)

        self._goto_home_button.raise_()  # overlaps the other widgets
        self._arrow_left.raise_()  # overlaps the other widgets

    def _add_arrow_left(self, layout):
        layout.addWidget(
            self._arrow_left,
            self._config.arrow_left.origin_y,
            self._config.arrow_left.origin_x,
            self._config.arrow_left.height,
            self._config.arrow_left.width
        )

    def _add_arrow_right(self, layout):
        layout.addWidget(
            self._arrow_right,
            self._config.arrow_right.origin_y,
            self._config.arrow_right.origin_x,
            self._config.arrow_right.height,
            self._config.arrow_right.width
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

    def _add_drink_image(self, layout):
        layout.addWidget(
            self._drink_image,
            self._config.drink_image.origin_y,
            self._config.drink_image.origin_x,
            self._config.drink_image.height,
            self._config.drink_image.width,
        )

    def scroll_left(self):
        self.current_cocktail_index = max(0, self.current_cocktail_index - 1)
        self.swap_pages()

    def scroll_right(self):
        highest_possible_index = len(self._database.cocktail_names) - 1
        self.current_cocktail_index = min(highest_possible_index, self.current_cocktail_index + 1)
        self.swap_pages()

    def swap_pages(self):
        drink_title = self._drink_title
        cocktail_title_text = self._database.cocktail_names[self.current_cocktail_index]
        drink_title.set_text(cocktail_title_text)

        drink_ingredients = self._drink_ingredients
        cocktail_ingredients_text = self._database.cocktail_ingredients[self.current_cocktail_index]
        formatted_recipe_text = self._drink_ingredients.format_ingredients(cocktail_ingredients_text)
        drink_ingredients.set_text(formatted_recipe_text)

        drink_description = self._drink_description
        cocktail_description_text = self._database.cocktail_descriptions[self.current_cocktail_index]
        drink_description.setText(cocktail_description_text)

        drink_type = self._drink_type
        cocktail_type_text = self._database.cocktail_types_unsorted[self.current_cocktail_index]
        formatted_type_text = self._drink_type.format_type(cocktail_type_text)
        drink_type.setText(formatted_type_text)

        drink_image = self._drink_image
        cocktail_image_data = self._database.cocktail_images[self.current_cocktail_index]
        drink_image.update_image(cocktail_image_data)

