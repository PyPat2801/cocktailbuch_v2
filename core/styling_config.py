from dataclasses import dataclass

@dataclass
class ArrowBarStyle:
    background: str = "background-color: white; border: 1px solid white"


@dataclass
class SheetLeftStyle:
    drink_title: str = """
        color: white;
        background-color: transparent;
        font-family: "Brush Script MT", "Segoe Script", "Cursive", "sans-serif";
        font-weight: bold;
        font-size: {font_size}px;
    """

    drink_ingredients: str = """
        QScrollArea {{
            border: 1px solid white;
            background-color: transparent;
        }}

        QScrollArea > QWidget {{
            background-color: transparent;
        }}

        QLabel {{
            color: white;
            background-color: gray;
            font-size: {font_size}px;
        }}
    """
    drink_description: str = """
        color: white;
        background-color: transparent;
        font-size: {font_size}px;
    """
    drink_type: str = drink_title


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