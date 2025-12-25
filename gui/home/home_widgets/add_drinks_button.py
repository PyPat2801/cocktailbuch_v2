from .home_button import HomeButton


class AddDrinksButton(HomeButton):
    def __init__(self, path):
        super().__init__(
            path,
            styling="background-color: transparent; border: none;",
            display_image_filename="find_by_pic.png"
        )
