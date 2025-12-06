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
class AllDrinksConfig:
    goto_home_button: Rectangle
    sheet_left: Rectangle
    sheet_right: Rectangle


@dataclass
class GuiConfig:
    window: Rectangle
    grid: GridSpan
    home_page: HomePageConfig
    all_drinks_page: AllDrinksConfig
    scaling_factor: float
