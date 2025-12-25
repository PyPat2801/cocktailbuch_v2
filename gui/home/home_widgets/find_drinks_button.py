from .home_button import HomeButton


class FindDrinksButton(HomeButton):
    def __init__(self, path):
        super().__init__(
            path,
            styling="background-color: transparent; border: none;",
            display_image_filename="find_drinks.png"
        )
