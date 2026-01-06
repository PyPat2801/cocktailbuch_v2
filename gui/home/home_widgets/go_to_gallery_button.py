from .base_button import BaseButton


class GoToGalleryButton(BaseButton):
    def __init__(self, path):
        super().__init__(
            path,
            styling="background-color: transparent; border: none;",
            display_image_filename="gallery.svg"
        )
