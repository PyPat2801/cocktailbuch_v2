from __future__ import annotations

import math

from PySide6.QtCore import Qt, QRectF, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QFontMetrics, QPainterPath, QPen, QPainter, QColor
from PySide6.QtWidgets import QLabel, QSizePolicy, QWidget, QGraphicsOpacityEffect

from core import SheetLeftStyle, FontDivisors


class _MiniRatingBadge(QWidget):
    """
    Kleines Badge: Stern oben, Zahl unten.
    Keine Datenbank-/Signal-Logik, statisch für den Start (z.B. "10").
    """
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._value_text = "—"

        self._star_fill = QColor("#FFEB66")
        self._star_outline = QColor("#FFEB66")
        self._star_outline.setAlpha(230)

        self._text_color = QColor("#FFFFFF")

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self._opacity_effect)

        self._fade_anim = QPropertyAnimation(self._opacity_effect, b"opacity", self)
        self._fade_anim.setDuration(300)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def set_value_text(self, text: str) -> None:
        text = str(text)

        if text == self._value_text:
            return

        self._value_text = text
        self._play_fade()
        self.update()

    def _play_fade(self) -> None:
        self._fade_anim.stop()
        self._opacity_effect.setOpacity(0.45)
        self._fade_anim.setStartValue(0.45)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.start()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        w = max(1, self.width())
        h = max(1, self.height())

        star_h = int(h * 0.62)
        text_h = h - star_h

        star_rect = QRectF(0, 0, w, star_h)
        text_rect = QRectF(0, star_h, w, text_h)

        pad = min(star_rect.width(), star_rect.height()) * 0.10
        inner = star_rect.adjusted(pad, pad, -pad, -pad)

        path = self._create_star_path(inner)

        outline_w = max(0.5, inner.width() * 0.04)
        pen = QPen(self._star_outline)
        pen.setWidthF(outline_w)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(self._star_fill)
        painter.drawPath(path)

        painter.setPen(self._text_color)

        f = QFont(self.font())
        f.setPointSizeF(max(6.0, text_h * 0.55))
        painter.setFont(f)

        painter.drawText(text_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, self._value_text)
        painter.end()


    @staticmethod
    def _create_star_path(rect: QRectF) -> QPainterPath:
        cx = rect.center().x()
        cy = rect.center().y()
        r_outer = min(rect.width(), rect.height()) / 2.0
        r_inner = r_outer * 0.42  # spitzer

        path = QPainterPath()
        for i in range(10):
            angle_deg = i * 36.0 - 90.0
            angle = math.radians(angle_deg)
            r = r_outer if i % 2 == 0 else r_inner
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)

        path.closeSubpath()
        return path


class DrinkTitle(QLabel):
    def __init__(self, styling: SheetLeftStyle):
        super().__init__()
        self._styling = styling
        self._label = QLabel(self)
        self._badge = _MiniRatingBadge(self)

    def initialize(self):
        self._set_style()
        self._update_font_size()
        self._reposition_badge()

    def _set_style(self):
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)
        self.setMinimumHeight(0)

        # Label: rendert den Titel
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self._badge.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._label.setGeometry(self.contentsRect())
        self._update_font_size()
        self._reposition_badge()

    def set_text(self, text: str):
        self._text = text or ""
        self._label.setText(self._text)
        self._update_font_size()
        self._reposition_badge()

    def set_badge_value_text(self, text: str) -> None:
        self._badge.set_value_text(text)

    def _update_font_size(self):
        text = (self._label.text() or "").strip()

        widget_width = max(1, self._label.contentsRect().width())
        profile = FontDivisors.get_active_font_profile_for_widget(self._label)
        divisor = profile["font_title"]
        font_size = int(widget_width / divisor)
        font_size = max(12, min(120, font_size))

        if text:
            reserve = 5
            target_width = max(1, widget_width - reserve)

            f = QFont(self._label.font())
            while font_size > 12:
                f.setPointSize(font_size)
                fm = QFontMetrics(f)
                if fm.horizontalAdvance(text) <= target_width:
                    break
                font_size -= 1

        style = self._styling.drink_title.format(font_size=font_size)
        self._label.setStyleSheet(style)

    def _reposition_badge(self) -> None:
        """
        Badge wird nicht in die nächste Grid-Zelle gelegt,
        sondern direkt hinter den gerenderten Text gesetzt.
        """
        text = (self._label.text() or "").strip()
        if not text:
            self._badge.hide()
            return

        self._badge.show()

        label_rect = self._label.contentsRect()
        lw = float(label_rect.width())
        lh = float(label_rect.height())

        # Badge-Größe in Relation zur Titelhöhe (klein gehalten)
        badge_h = max(10.0, lh * 0.55)
        badge_w = max(10.0, badge_h * 0.55)

        self._badge.resize(int(badge_w), int(badge_h))

        fm = QFontMetrics(self._label.font())
        text_w = float(fm.horizontalAdvance(text))

        # AlignCenter: Startposition des Textes in der Label-Fläche
        x_text_start = max(0.0, (lw - text_w) / 2.0)

        gap = max(2.0, lh * 0.06)  # kleiner Abstand zwischen Text und Badge

        x = x_text_start + text_w + gap
        y = (lh - badge_h) / 2.0

        # Clamping, falls der Titel sehr lang ist
        x = min(x, lw - badge_w)

        # Koordinaten relativ zur Label-Geometrie im Wrapper
        self._badge.move(int(label_rect.x() + x), int(label_rect.y() + y))
