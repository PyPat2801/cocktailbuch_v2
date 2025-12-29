from PySide6.QtWidgets import QWidget

from gui.goto_home_button import GotoHomeButton


class BaseLayer(QWidget):
    def __init__(self, config, path, goto_home_callback):
        super().__init__()

        self._config = config
        self._goto_home_button = GotoHomeButton(path, goto_home_callback)

    def initialize(self, layout):
        self._goto_home_button.initialize()
        self._add_goto_home_button(layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def _add_goto_home_button(self, layout):
        layout.addWidget(
            self._goto_home_button,
            self._config.goto_home_button.origin_y,
            self._config.goto_home_button.origin_x,
            self._config.goto_home_button.height,
            self._config.goto_home_button.width,
        )

