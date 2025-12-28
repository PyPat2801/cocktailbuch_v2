from .home_button import HomeButton


class AddDrinksButton(HomeButton):
    def __init__(self, path, goto_add_drinks_callback):
        super().__init__(
            path,
            styling="background-color: transparent; border: none;",
            display_image_filename="find_by_pic.png"
        )
        self._callback = goto_add_drinks_callback

    def _initialize_image_label(self):
        super()._initialize_image_label()

        if self._callback:
            self.clicked.connect(self._callback)
