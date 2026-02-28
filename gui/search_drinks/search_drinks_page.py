from gui.base_layer import BaseLayer

from PySide6.QtCore import Qt, QStringListModel
from PySide6.QtWidgets import QCompleter

from core import DataBase, SearchDrinksConfig, SearchDrinksStyle, ImagesSearchBy
from gui.search_drinks.search_drinks_widgets import SearchByDrinks, SearchByFavorites, \
    SearchByIngredients, SearchByCategories, SearchInput, DrinkThumbnails


class SearchDrinksPage(BaseLayer):
    def __init__(self, configuration: SearchDrinksConfig, styling: SearchDrinksStyle, path: str,
                 image_names: ImagesSearchBy, goto_home_callback, database: DataBase):
        super().__init__(configuration.goto_home_button, path, goto_home_callback)

        self._signals_connected = False
        self._thumbnails_loaded = False

        self._config = configuration
        self._styling = styling
        self._database = database
        self._path = path

        self.search_by_drinks = SearchByDrinks(path, styling.search_drinks_button_style, image_names.search_by_drinks)
        self.search_by_ingredients = SearchByIngredients(path, styling.search_ingredients_button_style, image_names.search_by_ingredients)
        self.search_by_categories = SearchByCategories(path, styling.search_categories_button_style, image_names.search_by_categories)
        self.search_by_favorites = SearchByFavorites(path, styling.search_favorites_button_style, image_names.search_by_favorites)

        self.search_input = SearchInput(styling.search_input_style)
        self.drink_thumbnails = DrinkThumbnails(styling.thumbnails_style)

    def initialize(self, layout):
        super().initialize(layout)
        self._initialize_all_widgets()
        self._add_all_drinks_widgets(layout)
        self._initialize_completer()
        self._connect_signals()

        image_paths = self._database.get_cocktail_attributes(attribute="image")
        self.drink_thumbnails.set_images_from_bytes(image_paths)

    def _initialize_all_widgets(self):
        self.search_by_drinks.initialize()
        self.search_by_ingredients.initialize()
        self.search_by_categories.initialize()
        self.search_by_favorites.initialize()

        self.search_input.initialize()
        self.search_input.setEnabled(False)

        self.drink_thumbnails.initialize()

    def _initialize_completer(self):
        self._drink_completer_model = QStringListModel(self)
        self._drink_completer = QCompleter(self._drink_completer_model, self)
        self._drink_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._drink_completer.setFilterMode(Qt.MatchFlag.MatchContains)

    def _add_all_drinks_widgets(self, layout):
        self._add_search_by_drinks(layout)
        self._add_search_by_ingredients(layout)
        self._add_search_by_categories(layout)
        self._add_search_by_favorites(layout)

        self._add_search_input(layout)
        self._add_drink_thumbnails(layout)
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

    def _add_drink_thumbnails(self, layout):
        layout.addWidget(
            self.drink_thumbnails,
            self._config.drink_thumbnails.origin_y,
            self._config.drink_thumbnails.origin_x,
            self._config.drink_thumbnails.height,
            self._config.drink_thumbnails.width
        )

    def _connect_signals(self) -> None:
        if self._signals_connected:
            return
        self.search_by_drinks.clicked.connect(self._on_search_by_drinks_clicked)
        self.search_by_ingredients.clicked.connect(self._on_search_by_ingredients_clicked)

        self._signals_connected = True

    def _on_search_by_drinks_clicked(self):
        self.search_input.setEnabled(True)
        self.search_input.setPlaceholderText("Drinks")
        self.search_input.setFocus()

        cocktail_names = self._database.get_cocktail_attributes(attribute="name")
        self._drink_completer_model.setStringList(cocktail_names)
        self.search_input.setCompleter(self._drink_completer)

    def _on_search_by_ingredients_clicked(self):
        self.search_input.setEnabled(True)
        self.search_input.setPlaceholderText("Ingredients")
        self.search_input.setFocus()

        cocktail_ingredients = self._database.get_cocktail_attributes(attribute="ingredients")
        self._drink_completer_model.setStringList(cocktail_ingredients)
        self.search_input.setCompleter(self._drink_completer)



