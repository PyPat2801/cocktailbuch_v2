from dataclasses import dataclass


@dataclass
class PathConfig:
    image_home_path: str
    image_all_drinks_path: str
    image_default_cocktails: str
    image_add_drinks_path: str
    image_search_drinks_path: str


@dataclass
class ImagesSearchBy:
    search_by_drinks: str
    search_by_categories: str
    search_by_ingredients: str
    search_by_favorites: str


@dataclass
class ImagesHome:
    go_to_all_drinks: str
    go_to_add_drinks: str
    go_to_search_drinks: str
    go_to_gallery: str
    go_to_inventory: str


@dataclass
class ImageNames:
    images_search_by: ImagesSearchBy
    images_home: ImagesHome




