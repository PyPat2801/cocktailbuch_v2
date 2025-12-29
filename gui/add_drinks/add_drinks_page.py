
from gui.add_drinks.add_drinks_widgets import TitleTemplate
from gui.base_layer import BaseLayer
from core import AddDrinksConfig, DataBase, AddDrinksStyle


class AddDrinksPage(BaseLayer):
    def __init__(self, configuration: AddDrinksConfig, styling: AddDrinksStyle, path: str, goto_home_callback, database: DataBase):
        super().__init__(configuration.goto_home_button, path, goto_home_callback)

        self._config = configuration
        self._styling = styling
        self._database = database

        self._drink_title = TitleTemplate(configuration.title_template)

    def initialize(self, layout):
        super().initialize(layout)

        self._drink_title.initialize()
        self._add_title_template(layout)
        self.setLayout(layout)

        self._goto_home_button.raise_()  # overlaps the other widgets

    def _add_title_template(self, layout):
        layout.addWidget(
            self._drink_title,
            self._config.title_template.origin_y,
            self._config.title_template.origin_x,
            self._config.title_template.height,
            self._config.title_template.width,
        )

