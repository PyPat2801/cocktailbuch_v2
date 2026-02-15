from gui.base_layer import BaseLayer

from core import DataBase, SearchDrinksConfig, SearchDrinksStyle, ImagesSearchBy
from gui.search_drinks.search_drinks_widgets import SearchByDrinks, SearchByFavorites, \
    SearchByIngredients, SearchByCategories, SearchInput


class SearchDrinksPage(BaseLayer):
    def __init__(self, configuration: SearchDrinksConfig, styling: SearchDrinksStyle, path: str,
                 image_names: ImagesSearchBy, goto_home_callback, database: DataBase):
        super().__init__(configuration.goto_home_button, path, goto_home_callback)

        self._config = configuration
        self._styling = styling
        self._database = database
        self._path = path

        self.search_by_drinks = SearchByDrinks(path, styling.search_drinks_button_style, image_names.search_by_drinks)
        self.search_by_ingredients = SearchByIngredients(path, styling.search_ingredients_button_style, image_names.search_by_ingredients)
        self.search_by_categories = SearchByCategories(path, styling.search_categories_button_style, image_names.search_by_categories)
        self.search_by_favorites = SearchByFavorites(path, styling.search_favorites_button_style, image_names.search_by_favorites)

        self.search_input = SearchInput(styling.search_input_style)

    def initialize(self, layout):
        super().initialize(layout)
        self._initialize_all_widgets()
        self._add_all_drinks_widgets(layout)

    def _initialize_all_widgets(self):
        self.search_by_drinks.initialize()
        self.search_by_ingredients.initialize()
        self.search_by_categories.initialize()
        self.search_by_favorites.initialize()

        self.search_input.initialize()

    def _add_all_drinks_widgets(self, layout):
        self._add_search_by_drinks(layout)
        self._add_search_by_ingredients(layout)
        self._add_search_by_categories(layout)
        self._add_search_by_favorites(layout)

        self._add_search_input(layout)
        self.setLayout(layout)

    def _add_search_by_drinks(self, layout):
        layout.addWidget(
            self.search_by_drinks,
            self._config.search_by_drinks.origin_y,
            self._config.search_by_drinks.origin_x,
            self._config.search_by_drinks.height,
            self._config.search_by_drinks.width
        )

    def _add_search_by_ingredients(self, layout):
        layout.addWidget(
            self.search_by_ingredients,
            self._config.search_by_ingredients.origin_y,
            self._config.search_by_ingredients.origin_x,
            self._config.search_by_ingredients.height,
            self._config.search_by_ingredients.width
        )

    def _add_search_by_categories(self, layout):
        layout.addWidget(
            self.search_by_categories,
            self._config.search_by_categories.origin_y,
            self._config.search_by_categories.origin_x,
            self._config.search_by_categories.height,
            self._config.search_by_categories.width
        )

    def _add_search_by_favorites(self, layout):
        layout.addWidget(
            self.search_by_favorites,
            self._config.search_by_favorites.origin_y,
            self._config.search_by_favorites.origin_x,
            self._config.search_by_favorites.height,
            self._config.search_by_favorites.width
        )

    def _add_search_input(self, layout):
        layout.addWidget(
            self.search_input,
            self._config.search_input.origin_y,
            self._config.search_input.origin_x,
            self._config.search_input.height,
            self._config.search_input.width
        )




