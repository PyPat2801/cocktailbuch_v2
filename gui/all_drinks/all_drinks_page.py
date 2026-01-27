from PySide6.QtWidgets import QMessageBox, QInputDialog, QLineEdit

from core import DataBase, AllDrinksConfig, AllDrinksStyle
from gui.all_drinks.drinks_widgets import ArrowBar
from gui.all_drinks.drinks_widgets.sheet_left import DrinkTitle, DrinkIngredients, \
    DrinkDescription, DrinkType, DrinkDelete, DrinkEdit, DrinkRandomise
from gui.all_drinks.drinks_widgets.sheet_right import DrinkImage, DrinkRatingStars
from gui.all_drinks.drinks_widgets.side_bar import SideBar

from gui.base_layer import BaseLayer


class AllDrinksPage(BaseLayer):
    def __init__(self, configuration: AllDrinksConfig, styling: AllDrinksStyle,  path: str, goto_home_callback, database: DataBase):
        super().__init__(configuration.goto_home_button, path, goto_home_callback)

        self._config = configuration
        self._styling = styling
        self._database = database
        self._path = path

        self.current_cocktail_index = 0

        self._arrow_left = ArrowBar("<=", self.scroll_left, styling.arrow_style)
        self._arrow_right = ArrowBar("=>", self.scroll_right, styling.arrow_style)

        self._drink_title = DrinkTitle(styling.sheet_left_style)
        self._drink_ingredients = DrinkIngredients(styling.sheet_left_style)
        self._drink_description = DrinkDescription(styling.sheet_left_style)
        self._drink_type = DrinkType(styling.sheet_left_style)

        self._drink_image = DrinkImage(self._database)
        self._drink_rating_stars = DrinkRatingStars(self._path)

        self._side_bar = SideBar(styling.side_bar_style)
        self._drink_delete = DrinkDelete(path, delete_callback=self._on_delete_clicked)
        self._drink_edit = DrinkEdit(path, edit_callback=self._on_edit_clicked)
        self._drink_randomise = DrinkRandomise(path, randomise_callback=self._on_randomise_clicked)

    def initialize(self, layout):
        super().initialize(layout)

        self._initialize_all_drinks_widgets()
        self._add_all_drinks_widgets(layout)

        self._drink_rating_stars.rating_committed.connect(self._on_rating_clicked)

        self.swap_pages()

    def _initialize_all_drinks_widgets(self):
        self._arrow_left.initialize()
        self._arrow_right.initialize()

        self._drink_title.initialize()
        self._drink_ingredients.initialize()
        self._drink_description.initialize()
        self._drink_type.initialize()

        self._drink_image.initialize()
        self._drink_rating_stars.initialize()

        self._side_bar.initialize()
        self._drink_delete.initialize()
        self._drink_edit.initialize()
        self._drink_randomise.initialize()

    def _add_all_drinks_widgets(self, layout):
        self._add_arrow_left(layout)
        self._add_arrow_right(layout)

        self._add_drink_title(layout)
        self._add_drink_ingredients(layout)
        self._add_drink_description(layout)
        self._add_drink_type(layout)

        self._add_drink_image(layout)
        self._add_drink_rating_stars(layout)

        self._add_side_bar(layout)
        self._add_drink_delete(layout)
        self._add_drink_edit(layout)
        self._add_drink_randomise(layout)

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

    def _add_drink_rating_stars(self, layout):
        layout.addWidget(
            self._drink_rating_stars,
            self._config.drink_rating_stars.origin_y,
            self._config.drink_rating_stars.origin_x,
            self._config.drink_rating_stars.height,
            self._config.drink_rating_stars.width,
        )

    def _add_drink_delete(self, layout):
        layout.addWidget(
            self._drink_delete,
            self._config.drink_delete.origin_y,
            self._config.drink_delete.origin_x,
            self._config.drink_delete.height,
            self._config.drink_delete.width,
        )

    def _add_drink_edit(self, layout):
        layout.addWidget(
            self._drink_edit,
            self._config.drink_edit.origin_y,
            self._config.drink_edit.origin_x,
            self._config.drink_edit.height,
            self._config.drink_edit.width,
        )

    def _add_drink_randomise(self, layout):
        layout.addWidget(
            self._drink_randomise,
            self._config.drink_randomise.origin_y,
            self._config.drink_randomise.origin_x,
            self._config.drink_randomise.height,
            self._config.drink_randomise.width,
        )

    def _add_side_bar(self, layout):
        layout.addWidget(
            self._side_bar,
            self._config.side_bar.origin_y,
            self._config.side_bar.origin_x,
            self._config.side_bar.height,
            self._config.side_bar.width,
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
        drink_description.set_text(cocktail_description_text)

        drink_type = self._drink_type
        cocktail_type_text = self._database.cocktail_types_unsorted[self.current_cocktail_index]
        formatted_type_text = self._drink_type.format_type(cocktail_type_text)
        drink_type.setText(formatted_type_text)

        drink_image = self._drink_image
        cocktail_image_data = self._database.cocktail_images[self.current_cocktail_index]
        drink_image.update_image(cocktail_image_data)

        self._drink_rating_stars.reset_rating()
        self._sync_rating_badge_from_cache()

    def on_show(self, jump_to_last: bool = False) -> None:
        self._database.refresh_cache()

        if len(self._database.cocktail_names) == 0:
            self.current_cocktail_index = 0
            return

        if jump_to_last:
            self.current_cocktail_index = len(self._database.cocktail_names) - 1
        else:
            self.current_cocktail_index = min(
                self.current_cocktail_index,
                len(self._database.cocktail_names) - 1
            )

        self.swap_pages()

    def reset_cocktail_index(self) -> None:
        self.current_cocktail_index = 0

    def reset_cocktail_view(self) -> None:
        self._database.refresh_cache()
        if len(self._database.cocktail_names) == 0:
            self.current_cocktail_index = 0
            self._clear_view()
            return
        self.current_cocktail_index = min(
            self.current_cocktail_index,
            len(self._database.cocktail_names) - 1
        )
        self.swap_pages()

    def reset_rating_view(self):
        self._drink_rating_stars.reset_rating()

    def _on_delete_clicked(self) -> None:

        if not self._database.cocktail_names:
            QMessageBox.information(self, "Löschen", "Es ist kein Cocktail vorhanden.")
            return

        cocktail_name = self._database.cocktail_names[self.current_cocktail_index]

        password, ok = QInputDialog.getText(
            self,
            "Cocktail löschen",
            f"Passwort eingeben, um „{cocktail_name}“ zu löschen:",
            QLineEdit.Password
        )
        if not ok:
            return

        if password != self._config.global_params.delete_password:
            QMessageBox.warning(self, "Löschen", "Passwort ist nicht korrekt.")
            return

        confirm = QMessageBox.question(
            self,
            "Cocktail löschen",
            f"Soll „{cocktail_name}“ wirklich gelöscht werden?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        deleted_rows = self._database.delete_cocktail(cocktail_name)
        if deleted_rows <= 0:
            QMessageBox.warning(self, "Löschen", "Der Cocktail konnte nicht gelöscht werden.")
            return

        if deleted_rows > 0:
            self.reset_cocktail_view()

    def _on_rating_clicked(self, stars: int) -> None:
        cocktail_names = self._database.cocktail_names[self.current_cocktail_index]

        new_avg = self._database.add_rating_for_cocktail(
            cocktail_name=cocktail_names,
            new_rating=stars  # nur ganze Sterne
        )

        self._database.refresh_cache()
        self._drink_title.set_badge_value_text(f"{new_avg:.1f}")

    def _sync_rating_badge_from_cache(self) -> None:
        avg = self._database.cocktail_ratings[self.current_cocktail_index]

        if avg is None:
            self._drink_title.set_badge_value_text("—")  # oder "" oder "0.0"
        else:
            self._drink_title.set_badge_value_text(f"{float(avg):.1f}")

    def _on_edit_clicked(self):
        pass

    def _on_randomise_clicked(self):
        pass

    def _clear_view(self) -> None:
        # Absicherung falls der letzte Cocktail gelöscht werden sollte. Damit beim Löschen der Code nicht crasht
        self._drink_title.set_text("")
        self._drink_ingredients.set_text("")
        self._drink_description.set_text("")
        self._drink_type.setText("")

        try:
            self._drink_image.clear_image()
        except AttributeError:
            self._drink_image._original_pixmap = None
            self._drink_image.drink_image.clear()



