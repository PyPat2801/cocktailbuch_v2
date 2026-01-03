from PySide6.QtWidgets import QApplication
import math


class FontDivisors:
    REF_WIDTH = 1920
    REF_HEIGHT = 1080

    # Referenz-Parametersatz (gültig für 1920x1080)
    BASE_FONT_DIVISORS = {
        "font_ingredients": 18,
        "font_title": 5,
        "font_type": 18,
        "font_description": 20,
        "font_home_text": 7,
    }

    @classmethod
    def get_active_font_profile_for_widget(cls, widget) -> dict:
        screen = widget.window().screen() if widget.window() else None
        if screen is None:
            screen = QApplication.primaryScreen()

        geo = screen.geometry()
        width, height = geo.width(), geo.height()

        return cls._derive_profile_from_reference(width)

    @classmethod
    def _derive_profile_from_reference(cls, screen_width: int) -> dict:
        scale = screen_width / cls.REF_WIDTH
        derived = {}
        for name, base_divisor in cls.BASE_FONT_DIVISORS.items():
            derived[name] = max(1, int(math.ceil(base_divisor * scale)))
        return derived
