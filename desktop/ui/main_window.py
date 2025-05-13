from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget, QStyle
import sys
from .main_page import MainPage
from .visualization_page import VisualizationPage
from .packages_page import PackagesPage
from .settings_page import SettingsPage
from .report_page import ReportPage
from .themes import light_theme, dark_theme, current_theme
from .translations import tr, current_language
from .widgets import NavButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оптимизация раскроя")
        self.setGeometry(100, 100, 1000, 700)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        layout = QHBoxLayout(self.central)

        self.navbar = QVBoxLayout()
        navbar_widget = QFrame()
        navbar_widget.setObjectName("Navbar")
        navbar_widget.setLayout(self.navbar)
        layout.addWidget(navbar_widget, 0)

        self.stack = QStackedWidget()  # сначала создаем стек
        layout.addWidget(self.stack, 1)

        # теперь безопасно добавляем страницы
        self.buttons = []
        self.stats_page = MainPage()
        self.visual_page = VisualizationPage()
        self.packages_page = PackagesPage()
        self.settings_page = SettingsPage(self.change_language, self.change_theme)
        self.report_page = ReportPage()

        # добавляем все страницы в стек
        self.stack.addWidget(self.stats_page)
        self.stack.addWidget(self.visual_page)
        self.stack.addWidget(self.packages_page)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.report_page)


        self.stack.setCurrentWidget(self.stats_page)

        self.buttons.append(NavButton(tr('statistics'), self.style().standardIcon(QStyle.SP_ComputerIcon), lambda: self.stack.setCurrentWidget(self.stats_page), self.buttons))
        self.buttons.append(NavButton(tr('visualization'), self.style().standardIcon(QStyle.SP_FileDialogListView), lambda: self.stack.setCurrentWidget(self.visual_page), self.buttons))
        self.buttons.append(NavButton(tr('packages'), self.style().standardIcon(QStyle.SP_FileDialogDetailedView), lambda: self.stack.setCurrentWidget(self.packages_page), self.buttons))
        self.buttons.append(NavButton(tr('settings'), self.style().standardIcon(QStyle.SP_DialogHelpButton), lambda: self.stack.setCurrentWidget(self.settings_page), self.buttons))
        self.buttons.append(NavButton(tr('report'), self.style().standardIcon(QStyle.SP_FileDialogContentsView), lambda: self.stack.setCurrentWidget(self.report_page), self.buttons))


        for btn in self.buttons:
            self.navbar.addWidget(btn)
        self.buttons[0].click()

        self.navbar.addStretch()
        self.apply_theme()

    def change_language(self, lang):
        from .translations import current_language
        current_language = lang
        self.close()
        self.__init__()
        self.show()

    def change_theme(self, theme):
        from .themes import current_theme
        current_theme = theme
        self.apply_theme()

    def apply_theme(self):
        from .themes import current_theme, light_theme, dark_theme
        self.setStyleSheet(light_theme if current_theme == 'light' else dark_theme)


def launch_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
