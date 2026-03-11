import html
import re

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QTextDocument
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem

from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QStyle


class Highlighter(QStyledItemDelegate):
    """
        Custom item delegate for the QCompleter popup that enables
        substring highlighting within autocomplete suggestions.

        This delegate replaces the default rendering mechanism of the
        QListView used by QCompleter. Instead of drawing plain text,
        each item is rendered via a QTextDocument, allowing rich-text
        formatting (HTML-based).

        Functional responsibilities:
        ----------------------------
        • Receives the current user input (search query) via set_query().
        • Performs case-insensitive substring matching using regular expressions.
        • Wraps matched substrings in HTML tags (e.g., <b>) to apply
          visual emphasis such as bold formatting.
        • Ensures consistent typography by inheriting the effective
          font (family, size, weight) from the view (option.font).
        • Applies the correct base text color depending on selection state.
        • Preserves selection background rendering and layout spacing.
        • Stabilizes row height via sizeHint() to prevent visual jitter.

        Design rationale:
        -----------------
        Qt's default item rendering does not support partial formatting
        within a single string. By leveraging QTextDocument and HTML,
        fine-grained control over substring styling is achieved while
        maintaining integration with Qt's palette and font system.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._query = "" # enthält den aktuellen Inputstring

    def set_query(self, text: str) -> None:
        self._query = text or ""

    def paint(self, painter, option: QStyleOptionViewItem, index):
        text = index.data(Qt.ItemDataRole.DisplayRole) or ""  # holt den Vorschlag aus dem Modell
        text_escaped = html.escape(str(text))  # verhindert Sonderzeichen in HTML Struktur

        q = self._query
        if q:
            pattern = re.compile(re.escape(q), re.IGNORECASE)  # sucht nach Teilstring

            def repl(m):
                return f"<span style='font-weight:700; color:#ffd166;'>{html.escape(m.group(0))}</span>"

            rich = pattern.sub(repl, text_escaped)
        else:
            rich = text_escaped

        selected = bool(option.state & QStyle.StateFlag.State_Selected)

        # Textfarbe aus Palette holen (normal/selektiert)
        base_color = option.palette.color(
            QPalette.ColorRole.HighlightedText if selected else QPalette.ColorRole.Text).name()

        html_text = f"<span style='color:{base_color};'>{rich}</span>"

        doc = QTextDocument()
        doc.setHtml(html_text)

        painter.save()

        if selected:
            painter.fillRect(option.rect, option.palette.highlight())

        painter.translate(option.rect.topLeft())
        painter.translate(10, 6)
        doc.setTextWidth(option.rect.width() - 20)
        doc.setDefaultFont(option.font)
        doc.drawContents(painter)

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index):
        base = super().sizeHint(option, index)
        h = option.fontMetrics.height() + 12
        return QSize(base.width(), max(base.height(), h))