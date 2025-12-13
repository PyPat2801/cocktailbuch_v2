from dataclasses import dataclass

@dataclass
class ArrowBarStyle:
    background: str = "background-color: black; border: 1px solid black"


@dataclass
class SheetLeftStyle:
    drink_title: str = """
            color: white;
            background-color: transparent;
            font-family: "Brush Script MT", "Segoe Script", "Cursive", "sans-serif";
            font-weight: bold;
            font-size: {font_size}px;
        """

    drink_ingredients: str = drink_title
    drink_description: str = "background-color: green;border: 1px solid black"
    drink_type: str = "background-color: yellow;border: 1px solid black"


@dataclass
class HomeTextStyle:
    text_style: str = """
            color: white;
            font-family: "Brush Script MT", "Segoe Script", "Cursive", "sans-serif";
            font-weight: bold;
            font-size: {font_size}px;
        """


@dataclass
class AllDrinksStyle:
    arrow_style: ArrowBarStyle
    sheet_left_style: SheetLeftStyle


@dataclass
class HomeStyle:
    text_style: HomeTextStyle


@dataclass
class MainWindowStyle:
    all_drinks_style: AllDrinksStyle
    home_style: HomeStyle


@dataclass
class StylingConfig:
    main_window_style: MainWindowStyle