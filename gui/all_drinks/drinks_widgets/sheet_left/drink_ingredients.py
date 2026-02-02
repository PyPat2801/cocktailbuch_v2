from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel, QSizePolicy

from core import SheetLeftStyle, FontDivisors


class DrinkIngredients(QScrollArea):
    def __init__(self, styling: SheetLeftStyle):
        super().__init__()

        self._styling = styling

        self._content_widget = QWidget()
        self._content_layout = QVBoxLayout(self._content_widget)

        self._label = QLabel()
        self._content_layout.addWidget(self._label)

        self._current_font_size = None
        self._resize_scheduled = False

    def initialize(self):
        self._set_style()
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        # self._content_layout.setSpacing(0)
        self._label.setTextFormat(Qt.RichText)  # wegen <br> und Bullet-HTML
        self._label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self._configure_scroll_area()
        self._apply_style(font_size=24)

    def _set_style(self):
        self.setStyleSheet(self._styling.drink_ingredients)
        self._label.setStyleSheet(self._styling.drink_ingredients)
        self._label.setWordWrap(True)

    def _configure_scroll_area(self):
        self.setWidget(self._content_widget)
        self.setWidgetResizable(True)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(0)
        self.setMinimumWidth(0)

    def set_text(self, text: str):
        self._label.setText(text)
        self._schedule_resize_update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._schedule_resize_update()

    def _schedule_resize_update(self):
        if self._resize_scheduled:
            return
        self._resize_scheduled = True
        QTimer.singleShot(0, self._apply_resize_update)

    def _apply_resize_update(self):
        self._resize_scheduled = False

        vp_w = self.viewport().width()
        if vp_w > 0:
            self._label.setFixedWidth(vp_w)
        profile = FontDivisors.get_active_font_profile_for_widget(self)
        divisor = profile["font_ingredients"]
        font_size = int(self.width() / divisor)
        font_size = max(12, min(120, font_size))

        if font_size != self._current_font_size:
            self._current_font_size = font_size
            self._apply_style(font_size)

    def _apply_style(self, font_size: int):
        style = self._styling.drink_ingredients.format(font_size=font_size)
        self.setStyleSheet(style)

    @staticmethod
    def format_ingredients(ingredients_text: str):
        formatted_recipe_text = "<br>".join([f"{item.strip()}" for item in ingredients_text.split(",")])
        # formatted_recipe_text = "<br>".join([f"• {item.strip()}" for item in ingredients_text.split(",")])
        return formatted_recipe_text
