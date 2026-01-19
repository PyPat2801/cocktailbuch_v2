from __future__ import annotations

import math
from typing import Optional
from PySide6.QtCore import Signal, QRectF, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import Qt, QPainter, QColor, QPen, QBrush, QPainterPath
from PySide6.QtWidgets import QWidget


class DrinkRatingStars(QWidget):
    """
        UI-Widget zur Auswahl einer Sternbewertung.
        - Default-Anzeige: 2.5 Sterne
        - Hover: nur volle Sterne
        - Klick: finale Auswahl (int 1..5)
        """

    rating_committed = Signal(int)
    def __init__(self, path):
        super().__init__()
        self._path = path
        self._default_rating: float = 2.5
        self._current_rating: float = self._default_rating
        self._hover_rating: Optional[int] = None

        self._interactive: bool = True
        self._spacing_ratio: float = 0.06

        self.setMouseTracking(True)

        self._star_rects: list[QRectF] = []

        self._fill_color = QColor("#FFEB66")  # Gelb
        self._outline_color = QColor("#FFEB66")  # Gelb

        self._paint_scale = 1.0
        self._commit_anim = QPropertyAnimation(self, b"paintScale", self)
        self._commit_anim.setDuration(140)
        self._commit_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def initialize(self):
        self._outline_color.setAlpha(100)
        self._recalc_star_geometry()
        self.update()

    def reset_rating(self) -> None:
        self._current_rating = self._default_rating
        self._hover_rating = None
        self.update()

    def set_interactive(self, interactive: bool) -> None:
        self._interactive = bool(interactive)
        self._hover_rating = None
        self.setMouseTracking(self._interactive)
        self.update()

    def _get_paint_scale(self) -> float:
        return float(self._paint_scale)

    def _set_paint_scale(self, value: float) -> None:
        self._paint_scale = float(value)
        self.update()

    # diese Zeile sollte noch vor dem Konstruktor stehen, aber dann folgt ein "undefined reference" Fehler
    # für die Parameter. Python kann das aber lesen. Der Editor meckert da, nicht python.
    # Aufgrund von Lesbarkeit aber an dieser Stelle
    paintScale = Property(float, _get_paint_scale, _set_paint_scale)

    def _play_commit_pop(self) -> None:
        self._commit_anim.stop()
        self._commit_anim.setKeyValueAt(0.0, 1.0)
        self._commit_anim.setKeyValueAt(0.5, 1.06)
        self._commit_anim.setKeyValueAt(1.0, 1.0)
        self._commit_anim.start()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._recalc_star_geometry()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        if self._hover_rating is not None:
            self._hover_rating = None
            self.update()

    def mouseMoveEvent(self, event) -> None:
        if not self._interactive:
            return

        hovered = self._rating_from_pos(event.position().x(), event.position().y())
        if hovered != self._hover_rating:
            self._hover_rating = hovered
            self.update()

    def mousePressEvent(self, event) -> None:
        if not self._interactive:
            return

        if event.button() == Qt.MouseButton.LeftButton:
            clicked = self._rating_from_pos(event.position().x(), event.position().y())
            if clicked is not None:
                self._current_rating = float(clicked)
                self._hover_rating = None
                self._play_commit_pop()
                self.update()

                self.rating_committed.emit(clicked)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        # Zentrierte Skalierung (nur visuell)
        cx = self.width() / 2.0
        cy = self.height() / 2.0
        painter.translate(cx, cy)
        painter.scale(self._paint_scale, self._paint_scale)
        painter.translate(-cx, -cy)

        # Hover: nur volle Sterne; ohne Hover: Default darf halb sein
        if self._hover_rating is not None:
            rating = float(self._hover_rating)
            allow_half = False
        else:
            rating = float(self._current_rating)
            allow_half = True

        for idx, rect in enumerate(self._star_rects, start=1):
            state = self._star_state(idx, rating, allow_half)
            self._draw_star(painter, rect, state)

        painter.end()

    def _draw_star(self, painter: QPainter, rect: QRectF, state: str) -> None:
        pad = rect.width() * 0.06
        inner = rect.adjusted(pad, pad, -pad, -pad)

        path = self._create_star_path(inner)

        pen = QPen(self._outline_color)
        pen.setWidthF(max(0.5, inner.width() * 0.025))  # dünner Rand
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)

        if state == "empty":
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(path)
            return

        if state == "full":
            painter.setBrush(QBrush(self._fill_color))
            painter.drawPath(path)
            return

        # half
        painter.save()
        painter.setClipRect(QRectF(inner.x(), inner.y(), inner.width() / 2.0, inner.height()))
        painter.setBrush(QBrush(self._fill_color))
        painter.drawPath(path)
        painter.restore()

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)

    def _create_star_path(self, rect: QRectF) -> QPainterPath:
        """
        Erzeugt einen 5-zackigen Stern als Path.
        """
        cx = rect.center().x()
        cy = rect.center().y()
        r_outer = min(rect.width(), rect.height()) / 2.0
        r_inner = r_outer * 0.42  # Verhältnis bestimmt "Form" des Sterns

        path = QPainterPath()
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            r = r_outer if i % 2 == 0 else r_inner
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            path.moveTo(x, y) if i == 0 else path.lineTo(x, y)

        path.closeSubpath()
        return path

    def _recalc_star_geometry(self) -> None:
        w = max(1.0, float(self.width()))
        h = max(1.0, float(self.height()))

        # Star-Breite wird aus verfügbarer Breite bestimmt
        # spacing wird relativ zur Star-Breite gewählt (robust bei Resize)
        # w = 5*star + 4*spacing  => star = w / (5 + 4*ratio)
        star_w = w / (5.0 + 4.0 * self._spacing_ratio)
        spacing = star_w * self._spacing_ratio

        # tatsächliche Sternkante: begrenzt durch Höhe
        star_size = min(star_w, h)
        # bei niedriger Höhe wird spacing entsprechend reduziert
        if star_w > 0:
            spacing = min(spacing, max(0.0, (w - 5.0 * star_size) / 4.0))

        total_w = 5.0 * star_size + 4.0 * spacing
        x0 = (w - total_w) / 2.0
        y0 = (h - star_size) / 2.0

        rects: list[QRectF] = []
        x = x0
        for _ in range(5):
            rects.append(QRectF(x, y0, star_size, star_size))
            x += star_size + spacing

        self._star_rects = rects

    def _rating_from_pos(self, x: float, y: float) -> float | None:
        for i, rect in enumerate(self._star_rects):
            if rect.contains(x, y):
                return i + 1
        return None

    @staticmethod
    def _star_state(idx: int, rating: float, allow_half: bool) -> str:
        if rating >= idx:
            return "full"
        if allow_half and rating >= (idx - 0.5):
            return "half"
        return "empty"
