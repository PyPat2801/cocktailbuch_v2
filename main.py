import math
import sys
import logging
import os

from os.path import exists
from PySide6.QtWidgets import QApplication
from core import AllDrinksStyle, HomeStyle, HomeTextStyle, ArrowBarStyle, MainWindowStyle, SheetLeftStyle,\
    StylingConfig, DataBase, Utility, PathConfig, AddDrinksStyle, SheetRightStyle, SideBarStyle
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

    # database.reset_ratings()
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
        grid=GridSpan(width=50, height=32),
        home_page=HomePageConfig(
            home_icon=Rectangle(origin_x=43, origin_y=0, width=7, height=6),
            home_text=Rectangle(origin_x=10, origin_y=1, width=30, height=14),
            goto_drinks_button=Rectangle(origin_x=1, origin_y=18, width=7, height=9),
            goto_add_drinks_button=Rectangle(origin_x=11, origin_y=18, width=7, height=9),
            goto_find_drinks_button=Rectangle(origin_x=21, origin_y=18, width=7, height=9),
            goto_gallery_button=Rectangle(origin_x=31, origin_y=18, width=7, height=9),
            goto_inventory_button=Rectangle(origin_x=41, origin_y=18, width=7, height=9),
            label_drinks_text=Rectangle(origin_x=1, origin_y=28, width=7, height=3),
            label_add_text=Rectangle(origin_x=11, origin_y=28, width=7, height=3),
            label_search_text=Rectangle(origin_x=21, origin_y=28, width=7, height=3),
            label_gallery_text=Rectangle(origin_x=31, origin_y=28, width=7, height=3),
            label_inventory_text=Rectangle(origin_x=41, origin_y=28, width=7, height=3),
        ),
        all_drinks_page=AllDrinksConfig(
            goto_home_button=Rectangle(origin_x=43, origin_y=0, width=7, height=6),
            arrow_left=Rectangle(origin_x=0, origin_y=31, width=1, height=1),
            arrow_right=Rectangle(origin_x=49, origin_y=31, width=1, height=1),
            drink_title=Rectangle(origin_x=7, origin_y=0, width=21, height=7),
            drink_ingredients=Rectangle(origin_x=7, origin_y=7, width=21, height=12),
            drink_description=Rectangle(origin_x=7, origin_y=20, width=21, height=8),
            drink_type=Rectangle(origin_x=7, origin_y=29, width=21, height=3),
            drink_image=Rectangle(origin_x=31, origin_y=2, width=17, height=25),
            drink_rating_stars=Rectangle(origin_x=35, origin_y=28, width=8, height=3),
            drink_delete=Rectangle(origin_x=0, origin_y=25, width=5, height=6),
            drink_edit=Rectangle(origin_x=0, origin_y=18, width=5, height=6),
            drink_randomise=Rectangle(origin_x=0, origin_y=3, width=5, height=6),
            side_bar=Rectangle(origin_x=0, origin_y=0, width=5, height=32),
            global_params=GlobalParams(delete_password="1708")
        ),
        add_drinks_page=AddDrinksConfig(
            goto_home_button=Rectangle(origin_x=43, origin_y=0, width=7, height=6),
            title_template=Rectangle(origin_x=2, origin_y=0, width=21, height=7),
            ingredients_template=Rectangle(origin_x=2, origin_y=8, width=21, height=11),
            description_template=Rectangle(origin_x=2, origin_y=20, width=21, height=7),
            type_template=Rectangle(origin_x=2, origin_y=28, width=21, height=3),
            image_template=Rectangle(origin_x=29, origin_y=2, width=17, height=25),
            confirm_drink_button=Rectangle(origin_x=34, origin_y=28, width=7, height=3)
        )
    )
    return config


def create_styling():
    styling = StylingConfig(
        main_window_style=MainWindowStyle(
            all_drinks_style=AllDrinksStyle(
                sheet_left_style=SheetLeftStyle(),
                sheet_right_style=SheetRightStyle(),
                arrow_style=ArrowBarStyle(),
                side_bar_style=SideBarStyle(),
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
    database.add_column_if_not_exists(table_name="cocktails", column_name="rating", column_definition="REAL")
    database.add_column_if_not_exists(table_name="cocktails", column_name="rating_sum", column_definition="REAL")
    database.add_column_if_not_exists(table_name="cocktails", column_name="rating_count", column_definition="INTEGER")
    return database


if __name__ == "__main__":
    main()
