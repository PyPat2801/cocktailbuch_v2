from PySide6.QtGui import QFont

import re

from gui.base_layer import BaseLayer

from PySide6.QtCore import Qt, QStringListModel
from PySide6.QtWidgets import QCompleter

from core import DataBase, SearchDrinksConfig, SearchDrinksStyle, ImagesSearchBy
from gui.search_drinks.search_drinks_widgets import SearchByDrinks, SearchByFavorites, \
    SearchByIngredients, SearchByCategories, SearchInput, DrinkThumbnails

from .highlighter import Highlighter


class SearchDrinksPage(BaseLayer):
    def __init__(self, configuration: SearchDrinksConfig, styling: SearchDrinksStyle, path: str,
                 image_names: ImagesSearchBy, goto_home_callback, goto_all_drinks_callback, database: DataBase):
        super().__init__(configuration.goto_home_button, path, goto_home_callback)

        self._signals_connected = False
        self._thumbnails_loaded = False

        self._config = configuration
        self._styling = styling
        self._database = database
        self._path = path
        self._goto_all_drinks_callback = goto_all_drinks_callback

        self.search_by_drinks = SearchByDrinks(path, styling.search_drinks_button_style, image_names.search_by_drinks)
        self.search_by_ingredients = SearchByIngredients(path, styling.search_ingredients_button_style,
                                                         image_names.search_by_ingredients)
        self.search_by_categories = SearchByCategories(path, styling.search_categories_button_style,
                                                       image_names.search_by_categories)
        self.search_by_favorites = SearchByFavorites(path, styling.search_favorites_button_style,
                                                     image_names.search_by_favorites)

        self.search_input = SearchInput(styling.search_input_style)
        self.drink_thumbnails = DrinkThumbnails(styling.thumbnails_style)

        self._search_mode = "drinks"

        # Caches / Index
        self._all_images: list = []
        self._all_ingredients: list[str] = []
        self._all_names: list[str] = []
        self._all_ids: list[int] = []

        # self._drink_name_to_index: dict[str, set[int]] = {}
        self._drink_name_to_index: dict[str, int] = {}
        self._ingredient_token_to_indices: dict[str, set[int]] = {}
        self._ingredient_display: dict[str, str] = {}
        self._ingredient_tokens_sorted: list[str] = []

    def initialize(self, layout):
        super().initialize(layout)
        self._initialize_all_widgets()
        self._add_all_drinks_widgets(layout)
        self._initialize_completer()
        self._connect_signals()

        self._all_images = self._database.get_cocktail_attributes(attribute="image")
        self._all_ingredients = self._database.get_cocktail_attributes(attribute="ingredients")
        self._all_names = self._database.get_cocktail_attributes(attribute="name")
        self._all_ids = self._database.get_keys_from_db()

        self.drink_thumbnails.set_all_images_from_bytes(self._all_images)

        self._drink_name_to_index = self._build_name_index(self._all_names)
        self._ingredient_token_to_indices, self._ingredient_display = self._build_ingredient_index(self._all_ingredients)
        self._ingredient_tokens_sorted = sorted(self._ingredient_display.values(), key=lambda s: s.lower())

    def _initialize_all_widgets(self):
        self.search_by_drinks.initialize()
        self.search_by_ingredients.initialize()
        self.search_by_categories.initialize()
        self.search_by_favorites.initialize()

        self.search_input.initialize()
        self.search_input.setEnabled(False)

        self.drink_thumbnails.initialize()

    def _initialize_completer(self):
        self._drink_completer_model = QStringListModel(self)  # Modell kapselt Liste aus strings.
        self._drink_completer = QCompleter(self._drink_completer_model, self)  # Verbinde Model mit Completer
        self._drink_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)  # Groß/Kleinschreibung irrelevant
        self._drink_completer.setFilterMode(Qt.MatchFlag.MatchContains)  # suche nach input string "irgendwo", nicht nur am Anfang

        self._drink_completer.setMaxVisibleItems(5)
        self._drink_completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)  # Completion als Dropdown

        self._highlight_delegate = Highlighter(self._drink_completer.popup())  # Kümmert sich um den Style des Dropdowns
        self._drink_completer.popup().setItemDelegate(self._highlight_delegate)

        # bei jeder Eingabe Query aktualisieren
        self.search_input.textEdited.connect(self._on_input_edited) # aktueller Substring in _query speichern

        popup = self._drink_completer.popup()

        popup.setStyleSheet(self._styling.search_input_style.autocompleter_style)  # der eigentliche Stil des Dropdowns.
        # Wenn allerdings ein eigenes Delegate genutzt wird, wird color und font-family nicht mehr angewendet. Daher spezifizierung in Highlighter
        self.search_input.font_updated.connect(self._apply_completer_popup_font_from_input)  # update der fontsize auf die fontsize des Inputs bei Größenänderung
        self.search_input.setCompleter(self._drink_completer)

        self._drink_completer.activated.connect(self._on_completer_activated)

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

    # -------------------------
    # Ingredients: Indexaufbau
    # -------------------------

    @staticmethod
    def _build_ingredient_index(ingredient_rows: list[str]) -> tuple[dict[str, set[int]], dict[str, str]]:
        word_re = re.compile(r"[A-Za-zÄÖÜäöüß]+")
        stop = {"cl", "tl", "el", "ml", "l", "g", "kg"}

        index: dict[str, set[int]] = {}
        display: dict[str, str] = {}

        for i, row in enumerate(ingredient_rows):
            if not isinstance(row, str):
                continue

            for w in word_re.findall(row):
                key = w.lower()
                if len(key) < 2 or key in stop:
                    continue

                index.setdefault(key, set()).add(i)

                # Display-Schreibweise einmalig merken (erste gefundene Form)
                if key not in display:
                    display[key] = w
        return index, display

    def _build_name_index(self, names: list[str]) -> dict[str, int]:
        index: dict[str, int] = {}
        for i, name in enumerate(names):
            if not isinstance(name, str):
                continue
            key = name.strip().lower()
            if not key:
                continue
            # falls Namen eindeutig sind: erster Treffer genügt
            index.setdefault(key, i)
        return index

    # -------------------------
    # Mode / UI
    # -------------------------

    def _reset_search_state(self):
        self.search_input.clear()
        self.search_input.setEnabled(False)
        self.search_input.setPlaceholderText("Hier was auch immer eingeben...")

        self._drink_completer_model.setStringList([])  # Modell leeren. Completer bleibt bestehen
        self._highlight_delegate.set_query("")

        self.drink_thumbnails.reset_filter()

        self._search_mode = "drinks"

    def _apply_completer_popup_font_from_input(self):
        popup = self._drink_completer.popup()
        popup.setFont(QFont(self.search_input.font()))

    def _connect_signals(self) -> None:
        if self._signals_connected:
            return
        self.search_by_drinks.clicked.connect(self._on_search_by_drinks_clicked)
        self.search_by_ingredients.clicked.connect(self._on_search_by_ingredients_clicked)
        self._goto_home_button.clicked.connect(self._reset_search_state)
        self.drink_thumbnails.thumbnail_clicked.connect(self._on_thumbnail_clicked)

        self._signals_connected = True

    def _activate_search_mode(self, placeholder: str, items: list[str]):
        self.search_input.clear()
        self.search_input.setEnabled(True)
        self.search_input.setPlaceholderText(placeholder)
        self.search_input.setFocus()

        cleaned = [s.strip() for s in items if isinstance(s, str) and s.strip()]
        self._drink_completer_model.setStringList(cleaned)

        self._apply_completer_popup_font_from_input()
        self._highlight_delegate.set_query(self.search_input.text())

    def _on_search_by_drinks_clicked(self):
        self._search_mode = "drinks"
        self.drink_thumbnails.reset_filter()
        self._activate_search_mode("Drinks", self._all_names)

    def _on_search_by_ingredients_clicked(self):
        self._search_mode = "ingredients"
        self.drink_thumbnails.reset_filter()
        self._activate_search_mode("Ingredients", self._ingredient_tokens_sorted)

    def _on_thumbnail_clicked(self, index: int) -> None:
        if index < 0 or index >= len(self._all_ids):
            return

        cocktail_id = self._all_ids[index]
        self._leave_page(self._goto_all_drinks_callback, select_id=cocktail_id)

    # -------------------------
    # Completer-Integration
    # -------------------------

    def _on_completer_activated(self, completion: str):
        if self._search_mode == "ingredients":
            text = self.search_input.text()
            parts = text.split(" ")
            if not parts:
                new_text = completion
            else:
                parts[-1] = completion
                new_text = " ".join(parts)

            self.search_input.setText(new_text)
            self.search_input.setCursorPosition(len(new_text))

            self._filter_thumbnails_by_ingredient_token(completion)
            return

        key = (completion or "").strip().lower()
        index = self._drink_name_to_index.get(key)

        if index is None:
            return

        if 0 <= index < len(self._all_ids):
            cocktail_id = self._all_ids[index]
            self._leave_page(self._goto_all_drinks_callback, select_id=cocktail_id)

    def _on_input_edited(self, text: str) -> None:
        if self._search_mode == "ingredients":
            current = text.split(" ")[-1] if text else ""

            self._highlight_delegate.set_query(current)
            self._drink_completer.setCompletionPrefix(current)
            self._drink_completer.complete()
        else:
            self._highlight_delegate.set_query(text)

    def _filter_thumbnails_by_ingredient_token(self, token: str) -> None:
        key = (token or "").strip().lower()
        indices = self._ingredient_token_to_indices.get(key, set())
        self.drink_thumbnails.show_only_indices(indices)

    def _leave_page(self, navigate_callback, **kwargs) -> None:
        self._reset_search_state()
        navigate_callback(**kwargs)
