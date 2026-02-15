from .base_button import BaseButton


class GoToInventoryButton(BaseButton):
    def __init__(self, path, image_go_to_inventory):
        super().__init__(
            path,
            styling="background-color: transparent; border: none;",
            display_image_filename=image_go_to_inventory
        )
