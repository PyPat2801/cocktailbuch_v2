from dataclasses import dataclass


@dataclass
class ArrowBarStyle:
    background: str = "background-color: white; border: 1px solid white"


@dataclass
class SheetLeftStyle:
    drink_title: str = """
        QLabel {{
            color: white;
            background-color: transparent;
            font-family: "Brush Script MT", "Segoe Script", "Cursive", "sans-serif";
            font-weight: bold;
            font-size: {font_size}px;
        }}
        
        QLineEdit {{
            color: white;
            background-color: transparent;
            font-family: "Brush Script MT", "Segoe Script", "Cursive", "sans-serif";
            font-weight: bold;
            font-size: {font_size}px;
            border: 1px solid gray;
        }}
    """

    drink_ingredients: str = """
        QScrollArea {{
            background-color: transparent;
        }}

        QScrollArea > QWidget {{
            background-color: transparent;
        }}

        QLabel {{
            color: white;
            background-color: black;
            font-size: {font_size}px;
        }}
        QPlainTextEdit {{
            color: white;
            background-color: transparent;
            font-size: {font_size}px;
            border: 1px solid gray;
        }}
    """
    drink_description: str = """
        QScrollArea {{
            background-color: transparent;
            border-top: 2px solid #FFFFFF;
        }}

        QScrollArea > QWidget {{
            background-color: transparent;
        }}

        QLabel {{
            color: white;
            background-color: black;
            font-size: {font_size}px;
        }}
        QPlainTextEdit {{
            color: white;
            background-color: transparent;
            font-size: {font_size}px;
            border: 1px solid white;
        }}
    """
    drink_type: str = drink_title


@dataclass
class SheetRightStyle:
    drink_image: str = """
        color: gray;
        border: 3px solid gray;
        background-color: transparent;
        font-size: 30px;
    """

    confirm_button: str = """
            QPushButton {
                color: white;
                border: 3px solid gray;
                background-color: transparent;
                font-size: 30px;
                font-weight: bold;
            }

            QPushButton:hover {
                border-color: white;
            }

            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 30);
            }
            
            QPushButton:disabled {
                color: rgba(255, 255, 255, 80);
                border-color: rgba(255, 255, 255, 60);
                background-color: rgba(255, 255, 255, 10);
            }
        """


@dataclass
class SideBarStyle:
    background = """
            QLabel {
                background-color: #1E1E1E;
                border-right: 2px solid #FFFFFF;
            }
        """


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
    sheet_right_style: SheetRightStyle
    side_bar_style: SideBarStyle


@dataclass
class AddDrinksStyle:
    sheet_left_style: SheetLeftStyle
    sheet_right_style: SheetRightStyle


@dataclass
class HomeStyle:
    text_style: HomeTextStyle


@dataclass
class MainWindowStyle:
    all_drinks_style: AllDrinksStyle
    home_style: HomeStyle
    add_drinks_style: AddDrinksStyle


@dataclass
class StylingConfig:
    main_window_style: MainWindowStyle