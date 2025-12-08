import sqlite3
from typing import List
from core.utility import Utility


class DataBase:
    def __init__(self, file_name):
        self.conn = sqlite3.connect(file_name)
        self.cocktail_names: List[str] = self.get_cocktail_attributes("name")
        self.cocktail_types: List[str] = sorted(list(set(self.get_cocktail_attributes("type"))))
        self.cocktail_types_unsorted: List[str] = self.get_cocktail_attributes("type")
        self.cocktail_ingredients: List[str] = self.get_cocktail_attributes("ingredients")
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

        # buy soll durch ein button ersetzt werden, welcher die Flasche auf die Einkaufsliste setzt
        # wenn bei "available" ein nein steht, dann soll ein Button sichtbar sein um es auf die Einkaufsliste zu setzen
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

    def fill_database_with_default_inventory(self):
        c = self.conn.cursor()

        inventory_data = [
            ("Weißer Rum", "Captain Morgan", "Spirituose", "Ja", "Nein"),
            ("Batida de Coco", "Mangaroca", "Likör", "Nein", "Ja"),
            ("Himbeersirup", "Monin", "Sirup", "Ja", "Ja"),
        ]

        c.executemany('''
            INSERT OR IGNORE INTO inventory (name, brand, type, available, buy) VALUES (?, ?, ?, ?, ?)
        ''', inventory_data)

        self.conn.commit()

    def get_inventory(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM inventory")
        return c.fetchall()

    def insert_into_inventory(self, values):
        query = """
        INSERT INTO inventory (name, brand, type, available, buy)
        VALUES (?, ?, ?, ?, ?)
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, values)
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Fehler beim Einfügen in die Datenbank: {e}")
            return None

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

    def call_from_db(self, cocktail_name, key):
        c = self.conn.cursor()
        try:
            c.execute(f"SELECT {key} FROM cocktails WHERE name = ?", (cocktail_name,))
            row = c.fetchone()
            if row is not None:
                return row[0]
            else:
                print(f"Warning: It seems, cocktail with cocktail name '{cocktail_name}' does not "
                      f"provide a key value named: '{key}'.")
                return None
        except Exception as e:
            print(f"Error executing database query: {e}")
            return None

    def get_cocktail_attributes(self, attribute: str):
        c = self.conn.cursor()
        cocktail_attributes: List[str] = []
        try:
            c.execute(f"SELECT {attribute} FROM cocktails")
            cocktail_attributes = [row[0] for row in c.fetchall()]
        except sqlite3.OperationalError as e:
            print(str(e))
        return cocktail_attributes

    def delete_inventory_item_from_db(self, item_id):
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
            self.conn.commit()
        except sqlite3.ProgrammingError as e:
            print("Fehler beim Löschen aus der Datenbank:", e)

    def get_cocktail_data(self, cocktail_name):
        c = self.conn.cursor()
        c.execute("SELECT name, ingredients, description, type, image FROM cocktails WHERE name = ?", (cocktail_name,))
        row = c.fetchone()
        if row:
            return {
                "name": row[0],
                "ingredients": row[1],
                "description": row[2],
                "type": row[3],
                "image": row[4]
            }
        return None

    def update_cocktail_data(self, cocktail_data):
        c = self.conn.cursor()
        c.execute("""
            UPDATE cocktails
            SET name = ?, ingredients = ?, description = ?, type = ?, image = ?
            WHERE name = ?
        """, (cocktail_data["name"], cocktail_data["ingredients"], cocktail_data["description"], cocktail_data["type"],
              cocktail_data["image"], cocktail_data["name"]))
        self.conn.commit()

    def delete_cocktail(self, cocktail_name):
        c = self.conn.cursor()
        c.execute("DELETE FROM cocktails WHERE name = ?", (cocktail_name,))
        self.conn.commit()

    def add_recipe(self, recipe_data):
        c = self.conn.cursor()
        c.execute("INSERT INTO cocktails (name, ingredients, description, type, image) VALUES (?, ?, ?, ?, ?)",
                            (recipe_data['name'], recipe_data['ingredients'], recipe_data['description'],
                             recipe_data["type"], recipe_data['image']))
        self.conn.commit()

    def delete_inventory_table(self):
        query = "DROP TABLE IF EXISTS inventory"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim Löschen der Tabelle: {e}")


