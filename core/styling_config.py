from dataclasses import dataclass


label_style: str = """
            color: white;
            font-family: "Brush Script MT", "Segoe Script", "Cursive", "sans-serif";
            font-weight: bold;
            font-size: {font_size}px;
        """

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
            border: none;
            outline: none;
        }}
        
        QLineEdit {{
            color: white;
            background-color: transparent;
            font-family: "Brush Script MT", "Segoe Script", "Cursive", "sans-serif";
            font-weight: bold;
            font-size: {font_size}px;
            border: none;
            outline: none;
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
            border: 1px solid gray;
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
class SearchDrinksButtonStyle:
    buttons_style: str = "background-color: transparent; border: none;"


@dataclass
class SearchInputStyle:
    input_style: str = """
            QLineEdit {{
                color: white;
                background-color: transparent;
                font-family: "Brush Script MT", "Segoe Script", "Cursive", "sans-serif";
                font-weight: bold;
                font-size: {font_size}px;
                border: none;
                outline: none;
                border: 1px solid gray;
        }}
        """


@dataclass
class ThumbnailsStyle:
    background: str = "background-color: black;"
    thumbnail_item: str = """
            QLabel {
                border: 2px solid white;
                background-color: black;
            }
        """
    scrollbar: str = """
            QScrollBar:horizontal {
                background: black;      /* gesamte Scrollbar */
                height: 14px;
                border: 1px solid white;
            }
        
            QScrollBar::groove:horizontal {
                background: white;      /* Bereich hinter dem Handle */
            }
        
            QScrollBar::handle:horizontal {
                background: gray;       /* Handle bleibt sichtbar */
                border-radius: 4px;
                min-width: 20px;
            }
        
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                background: none;
                border: none;
            }
        
            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: none;
            }
        """


@dataclass
class SearchDrinksStyle:
    search_drinks_button_style: SearchDrinksButtonStyle
    search_favorites_button_style: SearchDrinksButtonStyle
    search_ingredients_button_style: SearchDrinksButtonStyle
    search_categories_button_style: SearchDrinksButtonStyle
    search_input_style: SearchInputStyle
    thumbnails_style: ThumbnailsStyle
    label_style: str


@dataclass
class HomeTextStyle:
    text_style: str = label_style


@dataclass
class HomeStyle:
    text_style: HomeTextStyle


@dataclass
class MainWindowStyle:
    home_style: HomeStyle
    all_drinks_style: AllDrinksStyle
    add_drinks_style: AddDrinksStyle
    search_drinks_style: SearchDrinksStyle


@dataclass
class StylingConfig:
    main_window_style: MainWindowStyle
