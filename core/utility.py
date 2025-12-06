import os


class Utility:

    @staticmethod
    def get_image_path(image_name, subfolder=""):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        if subfolder:
            path_to_image = os.path.join(parent_dir, "images", subfolder, image_name)
        else:
            path_to_image = os.path.join(parent_dir, "images", image_name)
        return path_to_image
