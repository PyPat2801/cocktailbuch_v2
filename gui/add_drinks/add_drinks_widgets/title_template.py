
from PySide6.QtWidgets import QLabel

from core import Rectangle


class TitleTemplate(QLabel):
    def __init__(self, config: Rectangle):
        super().__init__()
        self._config = config

    def initialize(self):
        self.setStyleSheet("""
                    QLabel {
                        border: 1px solid yellow;
                    }
                """)

