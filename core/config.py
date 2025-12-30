from dataclasses import dataclass


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
    add_drinks_button: Rectangle
    find_drinks_button: Rectangle


@dataclass
class AddDrinksConfig:
    goto_home_button: Rectangle
    title_template: Rectangle
    ingredients_template: Rectangle
    description_template: Rectangle
    type_template: Rectangle
    image_template: Rectangle


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


@dataclass
class GuiConfig:
    window: Rectangle
    grid: GridSpan
    home_page: HomePageConfig
    all_drinks_page: AllDrinksConfig
    add_drinks_page: AddDrinksConfig
