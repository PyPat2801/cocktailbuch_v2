from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QLabel, QSizePolicy
from core import Utility, ThumbnailsStyle


class DrinkThumbnails(QWidget):
    def __init__(self, styling: ThumbnailsStyle):
        super().__init__()

        self._styling = styling
        self._initialized = False
        self._scroll = None
        self._content = None
        self._content_layout = None

        self._thumbnail_labels: list[QLabel] = []
        self._original_pixmaps: list[QPixmap] = []

        self._spacing = 10
        self._margins = 0

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

    def clear(self) -> None:
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

    def set_images_from_bytes(self, images: list[bytes]) -> None:
        if not self._initialized:
            self.initialize()

        self.clear()
        if self._content_layout is None:
            return

        for data in images:
            lbl, pm = self._create_thumbnail_label_from_bytes(data)
            self._thumbnail_labels.append(lbl)
            self._original_pixmaps.append(pm)
            self._content_layout.addWidget(lbl)

        self._content_layout.addStretch(1)
        self._update_thumbnail_sizes()

    def _create_thumbnail_label_from_bytes(self, data: bytes) -> tuple[QLabel, QPixmap]:
        lbl = QLabel()
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

        for lbl, pm in zip(self._thumbnail_labels, self._original_pixmaps):
            lbl.setFixedSize(target)
            if not pm.isNull():
                lbl.setPixmap(Utility.scale_and_crop_center(pm, target))
            lbl.setScaledContents(False)