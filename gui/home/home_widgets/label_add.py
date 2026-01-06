from .base_text_label import BaseTextLabel
from core import FontDivisors, HomeTextStyle


class LabelAdd(BaseTextLabel):
    _base_style = HomeTextStyle.text_style

    def __init__(self):
        super().__init__(text="Hinzufügen",
                         styling=self._base_style)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_size()

    def _update_font_size(self):
        profile = FontDivisors.get_active_font_profile_for_widget(self)
        divisor = profile["font_home_label"]
        font_size = int(self.width() / divisor)
        font_size = max(12, min(120, font_size))
        style = self._base_style.format(font_size=font_size)
        self.setStyleSheet(style)
