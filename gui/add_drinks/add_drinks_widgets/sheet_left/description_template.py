from typing import Optional

from PySide6.QtWidgets import QPlainTextEdit, QSizePolicy

from PySide6.QtGui import QTextOption, QShortcut, QKeySequence, Qt, QTextCursor

from core import Rectangle, SheetLeftStyle, FontDivisors


class DescriptionTemplate(QPlainTextEdit):

    def __init__(self, config: Rectangle, styling: SheetLeftStyle):
        super().__init__()
        self._config = config
        self._styling = styling
        self._current_font_size: Optional[int] = None

        self._confirm_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)

    def initialize(self):
        self._set_style()
        self._update_font_size()

    def _set_style(self):
        self.setStyleSheet(self._styling.drink_description)

        # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setTabChangesFocus(True)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setPlaceholderText("Beschreibung...")

        # ✅ Default: horizontal zentrierte Textblöcke
        opt = self.document().defaultTextOption()
        opt.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.document().setDefaultTextOption(opt)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_size()

    def _update_font_size(self):
        profile = FontDivisors.get_active_font_profile_for_widget(self)
        divisor = profile["font_description"]
        font_size = int(self.width() / divisor)
        font_size = max(12, min(120, font_size))

        if self._current_font_size == font_size:
            return
        self._current_font_size = font_size

        style = self._styling.drink_description.format(font_size=font_size)
        self.setStyleSheet(style)

    def get_value(self) -> str:
        return self.toPlainText().strip()

    def set_value(self, value: str) -> None:
        if value is None:
            value = ""
        self.setPlainText(value)
        self._apply_center_alignment_to_document()

    def _apply_center_alignment_to_document(self) -> None:
        cursor = self.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)

        block_fmt = cursor.blockFormat()
        block_fmt.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        cursor.setBlockFormat(block_fmt)

        cursor.clearSelection()
        self.setTextCursor(cursor)

