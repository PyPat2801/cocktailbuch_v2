from dataclasses import dataclass


@dataclass()
class PathConfig:
    image_home_path: str
    image_all_drinks_path: str
    image_default_cocktails: str


