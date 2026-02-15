from .base_button import BaseButton


class GotoDrinksButton(BaseButton):
    def __init__(self, path, image_go_to_all_drinks, goto_all_drinks_callback):
        super().__init__(
            path, 
            styling="background-color: transparent; border: none;", 
            display_image_filename=image_go_to_all_drinks
        )
        self._callback = goto_all_drinks_callback

    def _initialize_image_label(self):
        super()._initialize_image_label()

        if self._callback:
            self.clicked.connect(self._callback)





