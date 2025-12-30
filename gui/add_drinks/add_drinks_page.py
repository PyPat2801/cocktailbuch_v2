
from gui.add_drinks.add_drinks_widgets import TitleTemplate, IngredientsTemplate, DescriptionTemplate, TypeTemplate, ImageTemplate
from gui.base_layer import BaseLayer
from core import AddDrinksConfig, DataBase, AddDrinksStyle


class AddDrinksPage(BaseLayer):
    def __init__(self, configuration: AddDrinksConfig, styling: AddDrinksStyle, path: str, goto_home_callback, database: DataBase):
        super().__init__(configuration.goto_home_button, path, goto_home_callback)

        self._config = configuration
        self._styling = styling
        self._database = database

        self._drink_title = TitleTemplate(configuration.title_template)
        self._drink_ingredients = IngredientsTemplate(configuration.ingredients_template)
        self._drink_description = DescriptionTemplate(configuration.description_template)
        self._drink_type = TypeTemplate(configuration.type_template)
        self._drink_image = ImageTemplate(configuration.image_template)

    def initialize(self, layout):
        super().initialize(layout)

        self._drink_title.initialize()
        self._drink_ingredients.initialize()
        self._drink_description.initialize()
        self._drink_type.initialize()
        self._drink_image.initialize()

        self._add_title_template(layout)
        self._add_ingredients_template(layout)
        self._add_description_template(layout)
        self._add_type_template(layout)
        self._add_image_template(layout)

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

    def _add_ingredients_template(self, layout):
        layout.addWidget(
            self._drink_ingredients,
            self._config.ingredients_template.origin_y,
            self._config.ingredients_template.origin_x,
            self._config.ingredients_template.height,
            self._config.ingredients_template.width,
        )

    def _add_description_template(self, layout):
        layout.addWidget(
            self._drink_description,
            self._config.description_template.origin_y,
            self._config.description_template.origin_x,
            self._config.description_template.height,
            self._config.description_template.width,
        )

    def _add_type_template(self, layout):
        layout.addWidget(
            self._drink_type,
            self._config.type_template.origin_y,
            self._config.type_template.origin_x,
            self._config.type_template.height,
            self._config.type_template.width,
        )

    def _add_image_template(self, layout):
        layout.addWidget(
            self._drink_image,
            self._config.image_template.origin_y,
            self._config.image_template.origin_x,
            self._config.image_template.height,
            self._config.image_template.width,
        )

