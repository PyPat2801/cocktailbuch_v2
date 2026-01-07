from pathlib import Path
import re

from gui.add_drinks.add_drinks_widgets import TitleTemplate, IngredientsTemplate, DescriptionTemplate, TypeTemplate, ImageTemplate, ConfirmDrinkButton
from gui.base_layer import BaseLayer
from core import AddDrinksConfig, DataBase, AddDrinksStyle


class AddDrinksPage(BaseLayer):
    def __init__(self, configuration: AddDrinksConfig, styling: AddDrinksStyle, path: str, goto_home_callback,
                 goto_all_drinks_callback, database: DataBase):

        self._goto_home_callback = goto_home_callback

        super().__init__(configuration.goto_home_button, path, self._on_goto_home_clicked)

        self._config = configuration
        self._styling = styling
        self._database = database
        self._goto_all_drinks_callback = goto_all_drinks_callback

        self._drink_title = TitleTemplate(configuration.title_template, styling.sheet_left_style)
        self._drink_ingredients = IngredientsTemplate(configuration.ingredients_template, styling.sheet_left_style)
        self._drink_description = DescriptionTemplate(configuration.description_template, styling.sheet_left_style)
        self._drink_type = TypeTemplate(configuration.type_template, styling.sheet_left_style)
        self._drink_image = ImageTemplate(configuration.image_template, styling.sheet_right_style)
        self._confirm_drink_button = ConfirmDrinkButton(configuration.confirm_drink_button, styling.sheet_right_style)

    def initialize(self, layout):
        super().initialize(layout)

        self._drink_title.initialize()
        self._drink_ingredients.initialize()
        self._drink_description.initialize()
        self._drink_type.initialize()
        self._drink_image.initialize()
        self._confirm_drink_button.initialize()

        self._add_title_template(layout)
        self._add_ingredients_template(layout)
        self._add_description_template(layout)
        self._add_type_template(layout)
        self._add_image_template(layout)
        self._add_confirm_drink_button(layout)

        self.setLayout(layout)
        self._goto_home_button.raise_()  # overlaps the other widgets

        self._set_confirm_button_status()

    def _set_confirm_button_status(self):
        self._confirm_drink_button.clicked.connect(self._on_confirm_clicked)
        self._confirm_drink_button.setEnabled(False)
        self._wire_validation_signals()
        self._update_confirm_button_state()

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

    def _add_confirm_drink_button(self, layout):
        layout.addWidget(
            self._confirm_drink_button,
            self._config.confirm_drink_button.origin_y,
            self._config.confirm_drink_button.origin_x,
            self._config.confirm_drink_button.height,
            self._config.confirm_drink_button.width,
        )

    def _on_confirm_clicked(self):
        recipe_data = self._collect_recipe_data()
        if recipe_data is None:
            return

        raw_ingredients = self._drink_ingredients.get_value()
        recipe_data["ingredients"] = self.ingredients_to_db_string(raw_ingredients)
        self._database.add_recipe(recipe_data)
        self._leave_page(
            self._goto_all_drinks_callback,
            jump_to_last=True
        )

    @staticmethod
    def ingredients_to_db_string(raw: str) -> str:
        lines = raw.splitlines()

        cleaned = []
        for line in lines:
            line = re.sub(r"^\s*[•\-\*]\s*", "", line).strip()
            if line:
                cleaned.append(line)

        return ", ".join(cleaned)

    def _collect_recipe_data(self):
        name = self._drink_title.get_value()
        ingredients = self._drink_ingredients.get_value()
        description = self._drink_description.get_value()
        drink_type = self._drink_type.get_value()

        image_bytes = self._get_image_bytes_from_template()

        if not name or not ingredients or not description or not drink_type:
            return None

        return {
            "name": name,
            "ingredients": ingredients,
            "description": description,
            "type": drink_type,
            "image": image_bytes,
        }

    def _get_image_bytes_from_template(self):
        path = self._drink_image.get_image_path()
        if not path:
            return None

        try:
            return Path(path).read_bytes()
        except OSError:
            return None

    def _leave_page(self, navigate_callback, **kwargs) -> None:
        self.reset_inputs()
        navigate_callback(**kwargs)

    def reset_inputs(self) -> None:
        self._drink_title.clear()
        self._drink_ingredients.clear()
        self._drink_description.clear()
        self._drink_type.clear()
        self._drink_image.clear()

        self._confirm_drink_button.setEnabled(False)

    def _on_goto_home_clicked(self) -> None:
        self._leave_page(self._goto_home_callback)

    def _wire_validation_signals(self) -> None:
        self._drink_title.textChanged.connect(self._update_confirm_button_state)
        self._drink_type.textChanged.connect(self._update_confirm_button_state)
        self._drink_ingredients.textChanged.connect(self._update_confirm_button_state)
        self._drink_description.textChanged.connect(self._update_confirm_button_state)
        self._drink_image.image_selected.connect(lambda _path: self._update_confirm_button_state())

    def _update_confirm_button_state(self) -> None:
        self._confirm_drink_button.setEnabled(self._all_inputs_valid())

    def _all_inputs_valid(self) -> bool:
        name_ok = bool(self._drink_title.get_value())
        raw_ingredients = self._drink_ingredients.get_value()
        ingredients_ok = bool(self.ingredients_to_db_string(raw_ingredients))
        description_ok = bool(self._drink_description.get_value())
        type_ok = bool(self._drink_type.get_value())
        image_ok = bool(self._drink_image.get_image_path())

        return name_ok and ingredients_ok and description_ok and type_ok and image_ok
