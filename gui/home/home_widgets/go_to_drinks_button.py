from PySide6.QtGui import Qt, QPixmap
from PySide6.QtWidgets import QPushButton, QSizePolicy, QLabel
from .home_button import HomeButton
from core.utility import Utility


class GotoDrinksButton(HomeButton):
    def __init__(self, path, goto_drinks_callback):
        super().__init__(
            path, 
            styling="background-color: transparent; border: none;", 
            display_image_filename="go_to_drinks.png"
        )
        self._callback = goto_drinks_callback

    def _initialize_image_label(self):
        super()._initialize_image_label()

        if self._callback:
            self.clicked.connect(self._callback)





