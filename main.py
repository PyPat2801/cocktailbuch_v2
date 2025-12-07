import sys
import logging

from PySide6.QtWidgets import QApplication
from core.database import DataBase
from core.styling_config import AllDrinksStyle, ArrowBarStyle, MainWindowStyle, SheetLeftStyle, StylingConfig
from gui.main_window import MainWindow

from core.config import *


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    app = QApplication(sys.argv)
    config = create_config()
    styling = create_styling()
    database = get_database()
    main_window = MainWindow(app, config, styling.main_window_style, database)

    main_window.initialize()
    main_window.show()

    sys.exit(app.exec())


def create_config():
    config = GuiConfig(
        window=Rectangle(100, 100, 800, 600),
        grid=GridSpan(width=50, height=20),
        home_page=HomePageConfig(
            home_icon=Rectangle(origin_x=40, origin_y=1, width=7, height=3),
            home_text=Rectangle(origin_x=10, origin_y=2, width=30, height=6),
            goto_drinks_button=Rectangle(origin_x=5, origin_y=10, width=8, height=5),
            add_drinks_button=Rectangle(origin_x=20, origin_y=10, width=8, height=5),
            find_drinks_button=Rectangle(origin_x=35, origin_y=10, width=8, height=5)
        ),
        all_drinks_page=AllDrinksConfig(
            goto_home_button=Rectangle(origin_x=40, origin_y=1, width=7, height=3),
            arrow_left=Rectangle(origin_x=1, origin_y=10, width=2, height=1),
            sheet_left=Rectangle(origin_x=2, origin_y=1, width=21, height=18),
            sheet_right=Rectangle(origin_x=24, origin_y=1, width=21, height=18),
        ),
        scaling_factor=0.5,
    )
    return config

def create_styling():
    styling = StylingConfig(
        main_window_style=MainWindowStyle(
            all_drinks_style=AllDrinksStyle(
                sheet_left_style=SheetLeftStyle(),
                arrow_style=ArrowBarStyle()
            )
        )
    )
    return styling

def get_database():
    return DataBase("cocktails.db")

if __name__ == "__main__":
    main()
