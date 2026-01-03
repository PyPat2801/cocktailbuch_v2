from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPlainTextEdit, QSizePolicy
from PySide6.QtGui import QShortcut, QKeySequence, Qt

from PySide6.QtGui import QTextOption

from core import Rectangle, SheetLeftStyle, FontDivisors


class IngredientsTemplate(QPlainTextEdit):
    """Mehrzeiliges Eingabefeld für Zutaten (Bullet-Liste).
    - Enter: neue Zeile + Bullet-Präfix
    - Ctrl+Enter: confirmed-Signal
    """

    confirmed = Signal(str)
    BULLET = "• "

    def __init__(self, config: Rectangle, styling: SheetLeftStyle):
        super().__init__()
        self._config = config
        self._styling = styling

        self._current_font_size: Optional[int] = None

        self._confirm_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self._confirm_shortcut.activated.connect(self._emit_confirmed)

    def initialize(self):
        self._set_style()
        self._update_font_size()

    def _set_style(self):
        self.setStyleSheet(self._styling.drink_ingredients)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setTabChangesFocus(True)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setPlaceholderText("Zutaten eingeben …")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_size()

    def focusInEvent(self, event):
        super().focusInEvent(event)
        # Differenzierung ist hier nötig, da sonst jedes mal wenn man rein klickt ein bulletpoint kommt
        if not self.toPlainText().strip():
            self._insert_bullet_at_cursor()
        else:
            self._insert_bullet_if_current_line_empty()

    def _insert_bullet_at_cursor(self):
        cursor = self.textCursor()
        cursor.insertText(self.BULLET)
        self.setTextCursor(cursor)

    def _insert_bullet_if_current_line_empty(self):
        cursor = self.textCursor()
        cursor.movePosition(cursor.MoveOperation.StartOfLine)

        cursor.select(cursor.SelectionType.LineUnderCursor)
        line_text = cursor.selectedText()
        if line_text.strip() == "":
            cursor.clearSelection()
            cursor.insertText(self.BULLET)
            self.setTextCursor(cursor)

    def _update_font_size(self):
        profile = FontDivisors.get_active_font_profile_for_widget(self)
        divisor = profile["font_ingredients"]

        widget_width = max(1, self.contentsRect().width())
        font_size = int(widget_width / divisor)
        font_size = max(12, min(120, font_size))

        if self._current_font_size == font_size:
            return
        self._current_font_size = font_size

        style = self._styling.drink_ingredients.format(font_size=font_size)
        self.setStyleSheet(style)

    def keyPressEvent(self, event):
        # Enter: neue Zeile + Bullet
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and not (
                event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
            cursor = self.textCursor()
            cursor.insertText("\n")
            cursor.insertText(self.BULLET)
            self.setTextCursor(cursor)
            return

        super().keyPressEvent(event)

    def get_value(self) -> str:
        return self.toPlainText().strip()

    def _emit_confirmed(self):
        self.confirmed.emit(self.get_value())
