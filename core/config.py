from dataclasses import dataclass


@dataclass
class GlobalParams:
    delete_password: str


@dataclass
class Rectangle:
    origin_x: int
    origin_y: int
    width: int
    height: int


@dataclass
class GridSpan:
    width: int
    height: int


@dataclass
class HomePageConfig:
    home_icon: Rectangle
    home_text: Rectangle

    goto_drinks_button: Rectangle
    goto_gallery_button: Rectangle
    goto_inventory_button: Rectangle
    goto_add_drinks_button: Rectangle
    goto_find_drinks_button: Rectangle

    label_drinks_text: Rectangle
    label_add_text: Rectangle
    label_search_text: Rectangle
    label_gallery_text: Rectangle
    label_inventory_text: Rectangle


@dataclass
class AddDrinksConfig:
    goto_home_button: Rectangle
    title_template: Rectangle
    ingredients_template: Rectangle
    description_template: Rectangle
    type_template: Rectangle
    image_template: Rectangle
    confirm_drink_button: Rectangle


@dataclass
class AllDrinksConfig:
    goto_home_button: Rectangle
    arrow_left: Rectangle
    arrow_right: Rectangle
    drink_title: Rectangle
    drink_ingredients: Rectangle
    drink_description: Rectangle
    drink_type: Rectangle
    drink_image: Rectangle
    drink_rating_stars: Rectangle
    drink_delete: Rectangle
    drink_edit: Rectangle
    drink_randomise: Rectangle
    side_bar: Rectangle
    global_params: GlobalParams


@dataclass
class GuiConfig:
    window: Rectangle
    grid: GridSpan
    home_page: HomePageConfig
    all_drinks_page: AllDrinksConfig
    add_drinks_page: AddDrinksConfig
