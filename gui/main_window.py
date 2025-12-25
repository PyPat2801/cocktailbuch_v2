from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QGridLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt
from core import GuiConfig, DataBase, MainWindowStyle, PathConfig
from gui.all_drinks import AllDrinksPage
from gui.home import HomePage


class MainWindow(QMainWindow):

    def __init__(self, application: QApplication, configuration: GuiConfig, paths: PathConfig, styling: MainWindowStyle, database: DataBase):
        super().__init__()
        self._config = configuration
        self._styling = styling
        self._app = application
        self._pages = QStackedWidget()
        self._home_page = HomePage(configuration.home_page,  styling.home_style, paths.image_home_path, self._show_all_drinks_page, database)
        self._all_drinks_page = AllDrinksPage(configuration.all_drinks_page, styling.all_drinks_style, paths.image_all_drinks_path, self._show_home_page, database)

    def initialize(self):
        self._set_window_format()
        home_layout = self._create_grid_layout()
        all_drinks_layout = self._create_grid_layout()

        # hier andere komponenten initialisieren
        self._home_page.initialize(home_layout)
        self._all_drinks_page.initialize(all_drinks_layout)

        # hierarchien definieren
        self._pages.addWidget(self._home_page)
        self._pages.addWidget(self._all_drinks_page)
        self.setCentralWidget(self._pages)

    def _set_window_format(self):
        self.setGeometry(
            self._config.window.origin_x,
            self._config.window.origin_y,
            self._config.window.width,
            self._config.window.height
        )

    def _create_grid_layout(self):
        layout = QGridLayout()
        self.set_layout_stretch(layout)
        layout.setSpacing(0)
        for y in range(self._config.grid.height):
            for x in range(self._config.grid.width):
                cell_label = self.create_coordinate_label(x, y)
                layout.addWidget(cell_label, y, x)
        return layout

    def create_coordinate_label(self, x: int, y: int):
        cell = QLabel()
        cell.setAlignment(Qt.AlignCenter)
        cell.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        cell.setStyleSheet("""
            QLabel {
                background-color: black;
            }
        """)
        return cell

    def set_layout_stretch(self, layout):
        for y in range(self._config.grid.height):
            layout.setRowStretch(y, 1)
        for x in range(self._config.grid.width):
            layout.setColumnStretch(x, 1)

    def _show_home_page(self):
        self._show_page(0)

    def _show_all_drinks_page(self):
        self._show_page(1)

    def _show_page(self, index):
        self._pages.setCurrentIndex(index)

