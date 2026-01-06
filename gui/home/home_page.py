from PySide6.QtWidgets import QWidget

from core import DataBase, HomePageConfig, HomeStyle
from gui.home.home_widgets import GotoDrinksButton, HomeIcon, GoToAddDrinksButton, \
    GoToFindDrinksButton, HomeText, GoToGalleryButton, GoToInventoryButton, \
    LabelDrinks, LabelSearch, LabelAdd, LabelGallery, LabelInventory


class HomePage(QWidget):
    def __init__(self, configuration: HomePageConfig, styling: HomeStyle, path: str, goto_all_drinks_callback, goto_add_drinks_callback, database: DataBase):
        super().__init__()
        self._config = configuration
        self._database = database
        self._styling = styling

        self.home_icon = HomeIcon(path)
        self.home_text = HomeText(styling.text_style)

        self.goto_all_drinks_button = GotoDrinksButton(path, goto_all_drinks_callback)
        self.goto_add_drinks_button = GoToAddDrinksButton(path, goto_add_drinks_callback)
        self.goto_find_drinks_button = GoToFindDrinksButton(path)
        self.goto_gallery_button = GoToGalleryButton(path)
        self.goto_inventory_button = GoToInventoryButton(path)

        self.label_drinks = LabelDrinks()
        self.label_add = LabelAdd()
        self.label_search = LabelSearch()
        self.label_gallery = LabelGallery()
        self.label_inventory = LabelInventory()

    def initialize(self, layout):
        self.home_icon.initialize()
        self.home_text.initialize()
        self.goto_all_drinks_button.initialize()
        self.goto_add_drinks_button.initialize()
        self.goto_find_drinks_button.initialize()
        self.goto_gallery_button.initialize()
        self.goto_inventory_button.initialize()

        self.label_drinks.initialize()
        self.label_add.initialize()
        self.label_search.initialize()
        self.label_gallery.initialize()
        self.label_inventory.initialize()

        self._add_home_icon(layout)
        self._add_home_text(layout)
        self._add_goto_drinks_button(layout)
        self._add_goto_gallery_button(layout)
        self._add_goto_inventory_button(layout)
        self._add_goto_add_drinks_button(layout)
        self._add_goto_find_drinks_button(layout)

        self._add_label_drinks_text(layout)
        self._add_label_add_text(layout)
        self._add_label_search_text(layout)
        self._add_label_gallery_text(layout)
        self._add_label_inventory_text(layout)
        self.setLayout(layout)

    def resizeEvent(self, event):
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
                self.goto_all_drinks_button,
                self._config.goto_drinks_button.origin_y,
                self._config.goto_drinks_button.origin_x,
                self._config.goto_drinks_button.height,
                self._config.goto_drinks_button.width,
        )

    def _add_goto_gallery_button(self, layout):
        layout.addWidget(
                self.goto_gallery_button,
                self._config.goto_gallery_button.origin_y,
                self._config.goto_gallery_button.origin_x,
                self._config.goto_gallery_button.height,
                self._config.goto_gallery_button.width,
        )

    def _add_goto_inventory_button(self, layout):
        layout.addWidget(
                self.goto_inventory_button,
                self._config.goto_inventory_button.origin_y,
                self._config.goto_inventory_button.origin_x,
                self._config.goto_inventory_button.height,
                self._config.goto_inventory_button.width,
        )

    def _add_goto_add_drinks_button(self, layout):
        layout.addWidget(
            self.goto_add_drinks_button,
            self._config.goto_add_drinks_button.origin_y,
            self._config.goto_add_drinks_button.origin_x,
            self._config.goto_add_drinks_button.height,
            self._config.goto_add_drinks_button.width,
        )

    def _add_goto_find_drinks_button(self, layout):
        layout.addWidget(
            self.goto_find_drinks_button,
            self._config.goto_find_drinks_button.origin_y,
            self._config.goto_find_drinks_button.origin_x,
            self._config.goto_find_drinks_button.height,
            self._config.goto_find_drinks_button.width,
        )

    def _add_home_text(self, layout):
        layout.addWidget(
            self.home_text,
            self._config.home_text.origin_y,
            self._config.home_text.origin_x,
            self._config.home_text.height,
            self._config.home_text.width,
        )

    def _add_label_drinks_text(self, layout):
        layout.addWidget(self.label_drinks,
                         self._config.label_drinks_text.origin_y,
                         self._config.label_drinks_text.origin_x,
                         self._config.label_drinks_text.height,
                         self._config.label_drinks_text.width,
        )

    def _add_label_add_text(self, layout):
        layout.addWidget(self.label_add,
                         self._config.label_add_text.origin_y,
                         self._config.label_add_text.origin_x,
                         self._config.label_add_text.height,
                         self._config.label_add_text.width,
        )

    def _add_label_search_text(self, layout):
        layout.addWidget(self.label_search,
                         self._config.label_search_text.origin_y,
                         self._config.label_search_text.origin_x,
                         self._config.label_search_text.height,
                         self._config.label_search_text.width,
        )

    def _add_label_gallery_text(self, layout):
        layout.addWidget(self.label_gallery,
                         self._config.label_gallery_text.origin_y,
                         self._config.label_gallery_text.origin_x,
                         self._config.label_gallery_text.height,
                         self._config.label_gallery_text.width,
        )

    def _add_label_inventory_text(self, layout):
        layout.addWidget(self.label_inventory,
                         self._config.label_inventory_text.origin_y,
                         self._config.label_inventory_text.origin_x,
                         self._config.label_inventory_text.height,
                         self._config.label_inventory_text.width,
        )

