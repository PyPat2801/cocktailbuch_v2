from __future__ import annotations

import sqlite3
from typing import List
from core.utility import Utility


class DataBase:
    def __init__(self, file_name):
        self.conn = sqlite3.connect(file_name)
        self.refresh_cache()

    def refresh_cache(self):
        self.cocktail_ids: List[int] = self.get_keys_from_db()
        self.cocktail_names: List[str] = self.get_cocktail_attributes("name")
        self.cocktail_types: List[str] = sorted(list(set(self.get_cocktail_attributes("type"))))
        self.cocktail_types_unsorted: List[str] = self.get_cocktail_attributes("type")
        self.cocktail_ingredients: List[str] = self.get_cocktail_attributes("ingredients")
        self.cocktail_descriptions: List[str] = self.get_cocktail_attributes("description")
        self.cocktail_images: List[bytes] = self.get_cocktail_attributes("image", is_image=True)
        self.cocktail_ratings: List[float | None] = self.get_cocktail_attributes("rating")
        self.cocktail_column_names: List[str] = self.get_column_names_from_db()

    def __del__(self):
        print("closing db")
        self.conn.close()

    def get_column_names_from_db(self):
        c = self.conn.cursor()
        c.execute("PRAGMA table_info(cocktails);")
        return [row[1] for row in c.fetchall()]

    def get_keys_from_db(self):
        c = self.conn.cursor()
        c.execute("SELECT id FROM cocktails ORDER BY id;")
        return [row[0] for row in c.fetchall()]

    def create_database(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS cocktails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                ingredients TEXT,
                description TEXT,
                type TEXT,
                image BLOB
            )
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        brand TEXT,
        type TEXT,
        available TEXT,
        buy TEXT
        )
        ''')
        self.conn.commit()

    def fill_database_with_default_cocktails(self, data):
        c = self.conn.cursor()
        for recipe, details in data.items():
            name = details['title']
            ingredients = ', '.join(details['ingredients'])
            description = details['description']
            type = details['type']

            c.execute('''
                INSERT INTO cocktails (name, ingredients, description, type)
                VALUES (?, ?, ?, ?)
            ''', (name, ingredients, description, type))

        self.conn.commit()
        self.cocktail_names = self.get_cocktail_attributes("name")

    def add_image_column(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute('ALTER TABLE cocktails ADD COLUMN image BLOB')
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("Column already exists")
            else:
                print(f"Exception: {e}")

    def add_image_to_db(self, file_name, cocktail_name, path):
        image_data = Utility.load_image(Utility.get_image_path(file_name, path))
        c = self.conn.cursor()
        c.execute('''
                UPDATE cocktails
                SET image = ?
                WHERE name = ?
            ''', (image_data, cocktail_name))
        self.conn.commit()

    def get_cocktail_attributes(self, attribute: str, is_image: bool = False):
        c = self.conn.cursor()
        cocktail_attributes = []
        try:
            if is_image:
                c.execute("SELECT image FROM cocktails ORDER BY id")
                cocktail_attributes = [row[0] for row in c.fetchall()]
            else:
                c.execute(f"SELECT {attribute} FROM cocktails ORDER BY id")
                cocktail_attributes = [row[0] for row in c.fetchall()]
        except sqlite3.OperationalError as e:
            print(str(e))
        return cocktail_attributes

    def add_recipe(self, recipe_data):
        c = self.conn.cursor()
        c.execute("INSERT INTO cocktails (name, ingredients, description, type, image) VALUES (?, ?, ?, ?, ?)",
                            (recipe_data['name'], recipe_data['ingredients'], recipe_data['description'],
                             recipe_data["type"], recipe_data['image']))
        self.conn.commit()
        self.refresh_cache()

    def update_recipe(self, cocktail_id: int, recipe_data: dict) -> None:
        c = self.conn.cursor()
        c.execute(
            """
            UPDATE cocktails
            SET name = ?, ingredients = ?, description = ?, type = ?, image = ?
            WHERE id = ?
            """,
            (
                recipe_data["name"],
                recipe_data["ingredients"],
                recipe_data["description"],
                recipe_data["type"],
                recipe_data["image"],
                cocktail_id,
            )
        )
        self.conn.commit()
        self.refresh_cache()

    def delete_cocktail(self, cocktail_name: str) -> int:
        c = self.conn.cursor()
        c.execute("DELETE FROM cocktails WHERE name = ?", (cocktail_name,))
        deleted_rows = c.rowcount
        self.conn.commit()
        return deleted_rows

    def add_column_if_not_exists(self, table_name: str, column_name: str, column_definition: str) -> None:
        cursor = self.conn.cursor()

        # bestehende Spalten abfragen
        cursor.execute(f"PRAGMA table_info({table_name});")
        existing_columns = {row[1] for row in cursor.fetchall()}

        if column_name in existing_columns:
            return

        alter_sql = (
            f"ALTER TABLE {table_name} "
            f"ADD COLUMN {column_name} {column_definition};"
        )

        cursor.execute(alter_sql)
        self.conn.commit()

    def add_rating_for_cocktail(self, cocktail_name: str, new_rating: int) -> float:
        c = self.conn.cursor()

        c.execute(
            "SELECT rating_sum, rating_count FROM cocktails WHERE name = ?",
            (cocktail_name,)
        )
        row = c.fetchone()

        if row is None:
            raise ValueError(f"No cocktail found with name='{cocktail_name}'")

        rating_sum = row[0] if row and row[0] is not None else 0.0
        rating_count = row[1] if row and row[1] is not None else 0

        rating_sum = float(rating_sum) + float(new_rating)
        rating_count = int(rating_count) + 1
        avg = rating_sum / rating_count

        c.execute(
            """
            UPDATE cocktails
            SET rating_sum = ?, rating_count = ?, rating = ?
            WHERE name = ?
            """,
            (rating_sum, rating_count, avg, cocktail_name)
        )
        self.conn.commit()

        return float(avg)

    def reset_ratings(self) -> None:
        c = self.conn.cursor()

        c.execute("""
            UPDATE cocktails
            SET
                rating = NULL,
                rating_sum = NULL,
                rating_count = NULL
        """)

        self.conn.commit()


