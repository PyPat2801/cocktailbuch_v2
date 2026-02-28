import os
import json

from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, Qt


class Utility:

    @staticmethod
    def load_json(file_name):
        path_to_file = Utility.get_json_file_path(file_name)
        with open(path_to_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    @staticmethod
    def get_json_file_path(file_name):
        if not file_name.endswith(".json"):
            file_name += ".json"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        return os.path.join(parent_dir, "data", file_name)

    @staticmethod
    def get_image_files_list(path):
        images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), path)
        return [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]

    @staticmethod
    def load_image(image_path):
        with open(image_path, 'rb') as file:
            image_data = file.read()
        return image_data

    @staticmethod
    def get_image_path(image_name, path, subfolder=""):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        if subfolder:
            path_to_image = os.path.join(parent_dir, path, subfolder, image_name)
        else:
            path_to_image = os.path.join(parent_dir, path, image_name)
        return path_to_image

    @staticmethod
    def scale_and_crop_center(pixmap: QPixmap, target: QSize) -> QPixmap:
        if pixmap.isNull():
            return pixmap

        original_size = pixmap.size()
        if original_size.width() <= 0 or original_size.height() <= 0:
            return pixmap

        original_ratio = original_size.width() / original_size.height()
        target_ratio = target.width() / target.height()

        if original_ratio > target_ratio:
            scaled_size = QSize(int(target.height() * original_ratio), target.height())
        else:
            scaled_size = QSize(target.width(), int(target.width() / original_ratio))

        scaled = pixmap.scaled(
            scaled_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        size_diff = scaled.size() - target

        x = int(0.5 * size_diff.width())
        y = int(0.5 * size_diff.height())

        return scaled.copy(x, y, target.width(), target.height())
