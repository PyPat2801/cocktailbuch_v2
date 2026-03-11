from PySide6.QtCore import Qt, QSize, QEvent, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QLabel, QSizePolicy
from core import Utility, ThumbnailsStyle

from functools import partial


class ClickableThumbnailLabel(QLabel):
    clicked = Signal()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class DrinkThumbnails(QWidget):
    thumbnail_clicked = Signal(int)

    def __init__(self, styling: ThumbnailsStyle):
        super().__init__()

        self._styling = styling
        self._initialized = False
        self._scroll = None
        self._content = None
        self._content_layout = None

        # Cache: einmal erzeugen, dann nur noch visible toggeln
        self._thumbnail_labels: list[ClickableThumbnailLabel] = []
        self._original_pixmaps: list[QPixmap] = []

        self._spacing = 10
        self._margins = 0

        self._stretch_added = False

    def initialize(self) -> None:
        if self._initialized:
            return
        self._set_style()
        self._build_ui()
        self._initialized = True

    def _set_style(self) -> None:
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet(self._styling.background)

    def _build_ui(self) -> None:
        self._scroll = QScrollArea(self)
        self._scroll.setStyleSheet(self._styling.scrollbar)
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        self._content = QWidget()
        self._content.setStyleSheet(self._styling.background)
        self._content_layout = QHBoxLayout(self._content)
        self._content_layout.setContentsMargins(1, self._margins, self._margins, self._margins)
        self._content_layout.setSpacing(self._spacing)
        self._content_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self._scroll.setWidget(self._content)
        self._scroll.viewport().installEventFilter(self)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self._scroll)

        self._scroll.horizontalScrollBar().rangeChanged.connect(lambda *_: self._update_thumbnail_sizes())

    # ---------------------------
    # Aufbau (einmalig)
    # ---------------------------
    def set_all_images_from_bytes(self, images: list[bytes]) -> None:
        """
        Builds and caches all thumbnail widgets once.
        Subsequent filtering must use show_only_indices / reset_filter.
        """
        if not self._initialized:
            self.initialize()

        if self._content_layout is None:
            return

        # Falls bereits aufgebaut: nicht erneut dekodieren
        if self._thumbnail_labels and len(self._thumbnail_labels) == len(images):
            self.reset_filter()
            self._update_thumbnail_sizes()
            return

        # Einmaliger Aufbau (hier ist clear() weiterhin sinnvoll)
        self._hard_clear_widgets()

        for i, data in enumerate(images):
            lbl, pm = self._create_thumbnail_label_from_bytes(data)
            lbl.clicked.connect(partial(self.thumbnail_clicked.emit, i))
            self._thumbnail_labels.append(lbl)
            self._original_pixmaps.append(pm)
            self._content_layout.addWidget(lbl)

        # Stretch nur einmal hinzufügen
        if not self._stretch_added:
            self._content_layout.addStretch(1)
            self._stretch_added = True

        self._update_thumbnail_sizes()

    def _hard_clear_widgets(self) -> None:
        """Clears layout widgets and cache completely (expensive path; avoid calling repeatedly)."""
        if self._content_layout is None:
            return

        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

        self._thumbnail_labels.clear()
        self._original_pixmaps.clear()
        self._stretch_added = False

    # ---------------------------
    # Filter (schnell)
    # ---------------------------
    def show_only_indices(self, indices: set[int]) -> None:
        """
        Shows only thumbnails whose position index is in 'indices'.
        Does not rebuild widgets or reload images.
        """
        if not self._thumbnail_labels:
            return
        for i, lbl in enumerate(self._thumbnail_labels):
            lbl.setVisible(i in indices)

        # Layout/scrollbar aktualisieren
        if self._content is not None:
            self._content.update()
        if self._scroll is not None:
            self._scroll.viewport().update()

    def reset_filter(self) -> None:
        """Shows all cached thumbnails."""
        if not self._thumbnail_labels:
            return

        for lbl in self._thumbnail_labels:
            lbl.setVisible(True)

        if self._content is not None:
            self._content.update()
        if self._scroll is not None:
            self._scroll.viewport().update()

    # ---------------------------
    # Intern
    # ---------------------------
    def _create_thumbnail_label_from_bytes(self, data: bytes) -> tuple[ClickableThumbnailLabel, QPixmap]:
        lbl = ClickableThumbnailLabel()
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setScaledContents(False)
        lbl.setStyleSheet(self._styling.thumbnail_item)

        pm = QPixmap()
        ok = pm.loadFromData(data)
        if not ok or pm.isNull():
            lbl.setText("No Image")

        return lbl, pm

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_thumbnail_sizes()

    def eventFilter(self, obj, event):
        if self._scroll is not None and obj is self._scroll.viewport():
            if event.type() == QEvent.Type.Resize:
                self._update_thumbnail_sizes()
        return super().eventFilter(obj, event)

    def _update_thumbnail_sizes(self) -> None:
        if not self._thumbnail_labels or self._scroll is None or self._content is None:
            return

        viewport = self._scroll.viewport()
        vw = max(1, viewport.width())
        vh = max(1, viewport.height())

        self._content.setFixedHeight(vh)

        total_spacing = 3 * self._spacing
        thumb_w = int((vw - total_spacing) / 4)
        thumb_w = max(60, thumb_w)

        reserve_h = 2
        thumb_h = max(60, vh - reserve_h)

        target = QSize(thumb_w, thumb_h)

        # Wichtig: Pixmap scaling nur bei Resize, nicht bei Filter
        for lbl, pm in zip(self._thumbnail_labels, self._original_pixmaps):
            lbl.setFixedSize(target)
            if not pm.isNull():
                lbl.setPixmap(Utility.scale_and_crop_center(pm, target))
            lbl.setScaledContents(False)