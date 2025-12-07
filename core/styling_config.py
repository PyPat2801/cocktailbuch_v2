from dataclasses import dataclass

@dataclass
class ArrowBarStyle:
    background: str = "background-color: black; border: 1px solid black"


@dataclass
class SheetLeftStyle:
    sheet_style: str = """QLabel { background-color: red;border: 1px solid black; }"""


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