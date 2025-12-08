from dataclasses import dataclass

@dataclass
class ArrowBarStyle:
    background: str = "background-color: black; border: 1px solid black"


@dataclass
class SheetLeftStyle:
    drink_title: str = "background-color: red;border: 1px solid black"
    drink_ingredients: str = "background-color: blue;border: 1px solid black"
    drink_description: str = "background-color: green;border: 1px solid black"
    drink_type: str = "background-color: yellow;border: 1px solid black"


@dataclass
class AllDrinksStyle:
    arrow_style: ArrowBarStyle
    sheet_left_style: SheetLeftStyle


@dataclass
class MainWindowStyle:
    all_drinks_style: AllDrinksStyle


@dataclass
class StylingConfig:
    main_window_style: MainWindowStyle