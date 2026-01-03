import math
import sys
import logging
import os

from os.path import exists
from PySide6.QtWidgets import QApplication
from core import AllDrinksStyle, HomeStyle, HomeTextStyle, ArrowBarStyle, MainWindowStyle, SheetLeftStyle,\
    StylingConfig, DataBase, Utility, PathConfig, AddDrinksStyle, SheetRightStyle
from gui.main_window import MainWindow

from core.config import *


def main():
    db_filename = "cocktails.db"
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    app = QApplication(sys.argv)
    config = create_config()
    styling = create_styling()
    paths = create_path_config()

    if any(arg.startswith("--new-db") for arg in sys.argv):
        if exists(db_filename):
            os.remove(db_filename)
        database = create_default_database(db_name=db_filename, path=paths.image_default_cocktails)
    else:
        database = get_database(db_filename)

    main_window = MainWindow(app, config, paths, styling.main_window_style, database)

    main_window.initialize()
    main_window.show()

    sys.exit(app.exec())


def set_app_resolution() -> tuple[int, int]:
    screen = QApplication.primaryScreen()
    geometry = screen.availableGeometry()

    width = math.ceil(geometry.width() * 0.7)
    height = math.ceil(geometry.height() * 0.7)

    return width, height


def create_config():
    window_width, window_height = set_app_resolution()
    config = GuiConfig(
        window=Rectangle(100, 100, window_width, window_height),
        grid=GridSpan(width=50, height=30),
        home_page=HomePageConfig(
            home_icon=Rectangle(origin_x=43, origin_y=0, width=7, height=5),
            home_text=Rectangle(origin_x=10, origin_y=1, width=30, height=13),
            goto_drinks_button=Rectangle(origin_x=1, origin_y=18, width=7, height=8),
            add_drinks_button=Rectangle(origin_x=15, origin_y=18, width=7, height=8),
            find_drinks_button=Rectangle(origin_x=29, origin_y=18, width=7, height=8)
        ),
        all_drinks_page=AllDrinksConfig(
            goto_home_button=Rectangle(origin_x=43, origin_y=0, width=7, height=5),
            arrow_left=Rectangle(origin_x=0, origin_y=15, width=1, height=1),
            arrow_right=Rectangle(origin_x=49, origin_y=15, width=1, height=1),
            drink_title=Rectangle(origin_x=2, origin_y=0, width=21, height=7),
            drink_ingredients=Rectangle(origin_x=2, origin_y=8, width=21, height=10),
            drink_description=Rectangle(origin_x=2, origin_y=19, width=21, height=8),
            drink_type=Rectangle(origin_x=2, origin_y=28, width=21, height=2),
            drink_image=Rectangle(origin_x=26, origin_y=1, width=21, height=28),
        ),
        add_drinks_page=AddDrinksConfig(
            goto_home_button=Rectangle(origin_x=43, origin_y=0, width=7, height=5),
            title_template=Rectangle(origin_x=2, origin_y=0, width=21, height=7),
            ingredients_template=Rectangle(origin_x=2, origin_y=8, width=21, height=10),
            description_template=Rectangle(origin_x=2, origin_y=19, width=21, height=8),
            type_template=Rectangle(origin_x=2, origin_y=28, width=21, height=2),
            image_template=Rectangle(origin_x=29, origin_y=1, width=17, height=24),
            confirm_drink_button=Rectangle(origin_x=34, origin_y=26, width=7, height=3)
        )
    )
    return config


def create_styling():
    styling = StylingConfig(
        main_window_style=MainWindowStyle(
            all_drinks_style=AllDrinksStyle(
                sheet_left_style=SheetLeftStyle(),
                sheet_right_style=SheetRightStyle(),
                arrow_style=ArrowBarStyle()
            ),
            home_style=HomeStyle(
                text_style=HomeTextStyle()
            ),
            add_drinks_style=AddDrinksStyle(
                sheet_left_style=SheetLeftStyle(),
                sheet_right_style=SheetRightStyle()
            )
        )
    )
    return styling


def create_path_config():
    paths_config = PathConfig(image_home_path='images/home',
                              image_all_drinks_path='images/all_drinks',
                              image_default_cocktails='images/default_cocktails',
                              image_add_drinks_path='images/add_drinks')
    return paths_config


def get_database(db_filename):
    return DataBase(db_filename)


def create_default_database(db_name, path):
    images_path = path
    database = get_database(db_name)  # empty db, will print "no such table: cocktails" error
    database.create_database()
    database.fill_database_with_default_cocktails(Utility.load_json("recipes"))

    # This is required to group image filenames with their respective cocktailnames to simplify
    # the image addition to the database
    # Alternatively one could add the file_name to the .json and skip the file_name entry
    # when displaying the QLabel for the left page
    standardized_cocktail_names = [cocktail_name.lower().replace(' ', '_') + '.jpg' for cocktail_name in
                                   database.cocktail_names]
    sorted_standardized_cocktail_names = [
        database.cocktail_names[standardized_cocktail_names.index(image_file_name)]
        for image_file_name in
        Utility.get_image_files_list(images_path)]

    for index, cocktail in enumerate(Utility.get_image_files_list(images_path)):
        database.add_image_to_db(file_name=cocktail, cocktail_name=sorted_standardized_cocktail_names[index],
                                 path=images_path)
    return database


if __name__ == "__main__":
    main()
