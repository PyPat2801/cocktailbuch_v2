import sqlite3
from typing import List
from core.utility import Utility


class DataBase:
    def __init__(self, file_name):
        self.conn = sqlite3.connect(file_name)
        self.refresh_cache()

    def refresh_cache(self):
        self.cocktail_names: List[str] = self.get_cocktail_attributes("name")
        self.cocktail_types: List[str] = sorted(list(set(self.get_cocktail_attributes("type"))))
        self.cocktail_types_unsorted: List[str] = self.get_cocktail_attributes("type")
        self.cocktail_ingredients: List[str] = self.get_cocktail_attributes("ingredients")
        self.cocktail_descriptions: List[str] = self.get_cocktail_attributes("description")
        self.cocktail_images: List[bytes] = self.get_cocktail_attributes("image", is_image=True)
        self.cocktail_keys: List[str] = self.get_keys_from_db()

    def __del__(self):
        print("closing db")
        self.conn.close()

    def get_keys_from_db(self):
        c = self.conn.cursor()
        c.execute("PRAGMA table_info(cocktails);")
        return [row[1] for row in c.fetchall()]

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
                c.execute("SELECT image FROM cocktails")
                cocktail_attributes = [row[0] for row in c.fetchall()]
            else:
                c.execute(f"SELECT {attribute} FROM cocktails")
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

    def delete_cocktail(self, cocktail_name: str) -> int:
        c = self.conn.cursor()
        c.execute("DELETE FROM cocktails WHERE name = ?", (cocktail_name,))
        deleted_rows = c.rowcount
        self.conn.commit()
        return deleted_rows


