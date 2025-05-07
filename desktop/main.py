import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                             QStackedWidget, QStyle, QLineEdit, QComboBox, QFormLayout, QFrame, QStatusBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# Локализация
translations = {
    'ru': {
        'statistics': "\U0001F4CA Главная Страница",
        'rolls': "Рулоны",
        'cutting_maps': "Карты раскроя",
        'packages': "Пакеты",
        'cutting_types': "Типы нарезки",
        'usage_and_waste': "Отходы и использование",
        'visualization': "Карты раскроя",
        'subtitle': "Оптимизация карт раскроя для минимизации отходов",
        'src_rolls': "Исходные рулоны",
        'target_rolls': "Целевые рулоны",
        'select': "Выбрать",
        'set': "Задать",
        'params': "Параметры",
        'new_map': "🞣 Новая карта",
        'export': "⎙ Экспорт",
        'optimize': "✂️ Оптимизировать",
        'result': "Результаты оптимизации\nЭффективность: 100%, Отходы: 0 мм",
        'theme': "Тема",
        'language': "Язык",
        'settings': "⚙️ Настройки",
        'api_url': "API URL",
        'port': "Порт"
    },
    'en': {
        'statistics': "\U0001F4CA Main Page",
        'rolls': "Rolls",
        'cutting_maps': "Cutting Maps",
        'packages': "Packages",
        'cutting_types': "Cutting Types",
        'usage_and_waste': "Usage and Waste",
        'visualization': "Cutting Layout",
        'subtitle': "Optimizing layouts to minimize waste",
        'src_rolls': "Source Rolls",
        'target_rolls': "Target Rolls",
        'select': "Select",
        'set': "Set",
        'params': "Parameters",
        'new_map': "🞣 New Map",
        'export': "⎙ Export",
        'optimize': "✂️ Optimize",
        'result': "Optimization Results\nEfficiency: 100%, Waste: 0 mm",
        'theme': "Theme",
        'language': "Language",
        'settings': "⚙️ Settings",
        'api_url': "API URL",
        'port': "Port"
    }
}

light_theme = """
    QWidget { background: #ffffff; color: #333333; }
    QPushButton { background-color: #007BFF; color: white; border-radius: 5px; padding: 6px; }
    QPushButton:checked { background-color: #6CA0DC; }
    QLabel { color: #333333; }
    QLineEdit { border: 1px solid #ccc; padding: 4px; border-radius: 3px; }
    QComboBox { padding: 4px; }
    QFrame#Header, QFrame#Footer, QFrame#Navbar { border: 1px solid black; }
"""

dark_theme = """
    QWidget { background: #121212; color: #E0E0E0; }
    QPushButton { background-color: #FFA726; color: black; border-radius: 5px; padding: 6px; }
    QPushButton:checked { background-color: #424242; }
    QLabel { color: #E0E0E0; }
    QLineEdit { background: #1e1e1e; border: 1px solid #424242; color: white; padding: 4px; border-radius: 3px; }
    QComboBox { background: #1e1e1e; color: white; padding: 4px; }
    QFrame#Header, QFrame#Footer, QFrame#Navbar { border: 1px solid white; }
"""

current_language = 'ru'
current_theme = 'light'


def tr(key):
    return translations[current_language].get(key, key)


class NavButton(QPushButton):
    def __init__(self, text, icon, callback, group):
        super().__init__(text)
        self.setIcon(icon)
        self.setCheckable(True)
        self.clicked.connect(lambda: self.activate(group, callback))
        self.setStyleSheet("padding: 10px; text-align: left;")

    def activate(self, group, callback):
        for btn in group:
            btn.setChecked(False)
        self.setChecked(True)
        callback()


class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(self.build_header())
        layout.addLayout(self.build_content())
        layout.addWidget(self.build_footer())

    def build_header(self):
        header = QFrame()
        header.setObjectName("Header")
        header.setLayout(QHBoxLayout())
        label = QLabel(tr('statistics'))
        label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        header.layout().addWidget(label)
        return header

    def build_footer(self):
        footer = QFrame()
        footer.setObjectName("Footer")
        footer.setLayout(QHBoxLayout())
        footer.layout().addWidget(QLabel("Footer content here"))
        return footer

    def build_content(self):
        vbox = QVBoxLayout()

        cards_layout = QHBoxLayout()
        self.add_stat_card(cards_layout, tr('rolls'), "48", "+4 за 24ч")
        self.add_stat_card(cards_layout, tr('cutting_maps'), "12", "+2 за 24ч")
        self.add_stat_card(cards_layout, tr('packages'), "36", "+8 за 24ч")
        vbox.addLayout(cards_layout)

        charts_layout = QHBoxLayout()
        charts_layout.addWidget(self.create_bar_chart())
        charts_layout.addWidget(self.create_donut_chart(tr('cutting_types'), [58, 42], ["Уголки", "Ленты"]))
        charts_layout.addWidget(self.create_donut_chart(tr('usage_and_waste'), [80, 20], ["Использовано", "Отходы"], ["green", "red"]))
        vbox.addLayout(charts_layout)

        return vbox

    def add_stat_card(self, layout, title, value, subtitle):
        card = QVBoxLayout()
        card.addWidget(QLabel(title))
        val = QLabel(value)
        val.setStyleSheet("font-size: 24px;")
        card.addWidget(val)
        sub = QLabel(subtitle)
        sub.setStyleSheet("color: gray;")
        card.addWidget(sub)
        w = QWidget()
        w.setLayout(card)
        w.setStyleSheet("background: #f5f5f5; border-radius: 10px; padding: 10px;")
        layout.addWidget(w)

    def create_bar_chart(self):
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.bar(["Пн", "Вт", "Ср", "Чт", "Пт"], [5, 7, 3, 8, 6], color='skyblue')
        return FigureCanvas(fig)

    def create_donut_chart(self, title, values, labels, colors=None):
        fig, ax = plt.subplots(figsize=(2.5, 2.5))
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90,
               colors=colors, wedgeprops=dict(width=0.4))
        ax.set_title(title)
        return FigureCanvas(fig)


class VisualizationPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(self.build_header())
        layout.addLayout(self.build_content())
        layout.addWidget(self.build_footer())

    def build_header(self):
        header = QFrame()
        header.setObjectName("Header")
        header.setLayout(QHBoxLayout())
        label = QLabel(tr('visualization'))
        label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        header.layout().addWidget(label)
        return header

    def build_footer(self):
        footer = QFrame()
        footer.setObjectName("Footer")
        footer.setLayout(QHBoxLayout())
        footer.layout().addWidget(QLabel("Footer content here"))
        return footer

    def build_content(self):
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel(tr('subtitle')))
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(tr('src_rolls')))
        hbox.addWidget(QLineEdit("0"))
        hbox.addWidget(QPushButton(tr('select')))
        hbox.addWidget(QLabel(tr('target_rolls')))
        hbox.addWidget(QLineEdit("3"))
        hbox.addWidget(QPushButton(tr('set')))
        hbox.addWidget(QPushButton(tr('params')))
        vbox.addLayout(hbox)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(QPushButton(tr('new_map')))
        btn_layout.addWidget(QPushButton(tr('export')))
        optimize_btn = QPushButton(tr('optimize'))
        optimize_btn.setStyleSheet("background-color: #007bff; color: white;")
        btn_layout.addWidget(optimize_btn)
        vbox.addLayout(btn_layout)

        result = QLabel(tr('result'))
        result.setStyleSheet("margin-top: 20px; font-weight: bold;")
        vbox.addWidget(result)
        return vbox


class SettingsPage(QWidget):
    def __init__(self, change_language, change_theme):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(self.build_header())

        form = QFormLayout()
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(['ru', 'en'])
        self.lang_combo.currentTextChanged.connect(change_language)
        form.addRow(tr('language'), self.lang_combo)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['light', 'dark'])
        self.theme_combo.currentTextChanged.connect(change_theme)
        form.addRow(tr('theme'), self.theme_combo)

        self.api_url_input = QLineEdit("http://localhost")
        form.addRow(tr('api_url'), self.api_url_input)

        self.port_input = QLineEdit("8000")
        form.addRow(tr('port'), self.port_input)

        layout.addLayout(form)
        layout.addWidget(self.build_footer())

    def build_header(self):
        header = QFrame()
        header.setObjectName("Header")
        header.setLayout(QHBoxLayout())
        label = QLabel(tr('settings'))
        label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        header.layout().addWidget(label)
        return header

    def build_footer(self):
        footer = QFrame()
        footer.setObjectName("Footer")
        footer.setLayout(QHBoxLayout())
        footer.layout().addWidget(QLabel("Footer content here"))
        return footer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оптимизация раскроя")
        self.setGeometry(100, 100, 1000, 700)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Готово")

        self.central = QWidget()
        self.setCentralWidget(self.central)
        layout = QHBoxLayout(self.central)

        self.navbar = QVBoxLayout()
        navbar_widget = QFrame()
        navbar_widget.setObjectName("Navbar")
        navbar_widget.setLayout(self.navbar)
        layout.addWidget(navbar_widget, 0)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack, 1)

        self.buttons = []
        self.stats_page = MainPage()
        self.visual_page = VisualizationPage()
        self.settings_page = SettingsPage(self.change_language, self.change_theme)

        self.stack.addWidget(self.stats_page)
        self.stack.addWidget(self.visual_page)
        self.stack.addWidget(self.settings_page)

        self.stack.setCurrentWidget(self.stats_page)

        icon = self.style().standardIcon(QStyle.SP_ComputerIcon)
        self.buttons.append(NavButton(tr('statistics'), icon, lambda: self.stack.setCurrentWidget(self.stats_page), self.buttons))
        icon2 = self.style().standardIcon(QStyle.SP_FileDialogListView)
        self.buttons.append(NavButton(tr('visualization'), icon2, lambda: self.stack.setCurrentWidget(self.visual_page), self.buttons))
        icon3 = self.style().standardIcon(QStyle.SP_DialogHelpButton)
        self.buttons.append(NavButton(tr('settings'), icon3, lambda: self.stack.setCurrentWidget(self.settings_page), self.buttons))

        for btn in self.buttons:
            self.navbar.addWidget(btn)
        self.buttons[0].click()

        self.navbar.addStretch()
        self.apply_theme()

    def change_language(self, lang):
        global current_language
        current_language = lang
        self.close()
        self.__init__()
        self.show()

    def change_theme(self, theme):
        global current_theme
        current_theme = theme
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(light_theme if current_theme == 'light' else dark_theme)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
