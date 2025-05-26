import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QFrame, QStackedWidget, QStyle,
    QDialog, QLabel, QLineEdit, QPushButton, QMessageBox
)
from datetime import datetime
from PyQt5.QtCore import Qt

from .login_page import CombinedLoginWindow
from .main_page import MainPage
from .visualization_page import VisualizationPage
from .packages_page import PackagesPage
from .settings_page import SettingsPage
from .report_page import ReportPage
from .widgets import NavButton
from .themes import light_theme, dark_theme, current_theme
from .translations import tr
from .users_page import UsersPage


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Имя пользователя")
        layout.addWidget(QLabel("Имя пользователя:"))
        layout.addWidget(self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        self.role = None
        self.user_id = None
        self.token = None
        self.username = None  # добавлено

    def handle_login(self):
        username = self.user_input.text()
        password = self.password_input.text()

        try:
            response = requests.post("http://localhost:8000/users/login", json={
                "username": username,
                "password": password
            })

            if response.status_code == 200:
                data = response.json()
                self.role = data.get("role")
                self.user_id = data.get("id")
                self.token = data.get("token")
                self.username = username  # сохраняем логин
                self.accept()
            else:
                QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль.")
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Сервер недоступен", "Не удалось подключиться к серверу.")


class MainWindow(QMainWindow):
    def __init__(self, user_role="operator", user_id=None, username="Пользователь"):
        super().__init__()
        self.user_role = user_role
        self.user_id = user_id
        self.username = username  # получаем логин

        self.setWindowTitle("Оптимизация раскроя")
        self.showMaximized()

        self.central = QWidget()
        self.setCentralWidget(self.central)
        layout = QHBoxLayout(self.central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.navbar = QVBoxLayout()
        navbar_widget = QFrame()
        navbar_widget.setObjectName("Navbar")
        navbar_widget.setLayout(self.navbar)
        navbar_widget.setFixedWidth(200)
        layout.addWidget(navbar_widget, 0)

        self.central_frame = QFrame()
        self.central_frame.setObjectName("CentralFrame")
        self.central_layout = QVBoxLayout(self.central_frame)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)
        layout.addWidget(self.central_frame, 1)

        self.stack = QStackedWidget()
        self.central_layout.addWidget(self.stack)

        # Приветствие
        greeting_label = QLabel(self.get_greeting())
        greeting_label.setStyleSheet("padding: 20px; font-size: 16px; font-weight: bold; color: #333;")
        self.navbar.addWidget(greeting_label)

        # Страницы
        self.buttons = []
        self.stats_page = MainPage()
        self.visual_page = VisualizationPage(user_id=self.user_id)
        self.packages_page = PackagesPage()
        self.report_page = ReportPage()
        self.settings_page = SettingsPage(self.change_language, self.change_theme)

        self.stack.addWidget(self.stats_page)
        self.stack.addWidget(self.visual_page)
        self.stack.addWidget(self.packages_page)
        self.stack.addWidget(self.report_page)
        self.stack.addWidget(self.settings_page)

        self.buttons.append(NavButton(tr('statistics'), self.style().standardIcon(QStyle.SP_ComputerIcon),
                                      lambda: self.stack.setCurrentWidget(self.stats_page), self.buttons))
        self.buttons.append(NavButton(tr('visualization'), self.style().standardIcon(QStyle.SP_FileDialogListView),
                                      lambda: self.stack.setCurrentWidget(self.visual_page), self.buttons))
        self.buttons.append(NavButton(tr('packages'), self.style().standardIcon(QStyle.SP_FileDialogDetailedView),
                                      lambda: self.stack.setCurrentWidget(self.packages_page), self.buttons))
        self.buttons.append(NavButton(tr('report'), self.style().standardIcon(QStyle.SP_FileDialogContentsView),
                                      lambda: self.stack.setCurrentWidget(self.report_page), self.buttons))
        self.buttons.append(NavButton(tr('settings'), self.style().standardIcon(QStyle.SP_DialogHelpButton),
                                      lambda: self.stack.setCurrentWidget(self.settings_page), self.buttons))
        self.buttons.append(NavButton(tr('creation'), self.style().standardIcon(QStyle.SP_FileDialogDetailedView),
                                      lambda: self.stack.setCurrentWidget(self.creation_page), self.buttons))
        self.buttons.append(NavButton(tr('reports'), self.style().standardIcon(QStyle.SP_FileDialogContentsView),
                                      lambda: self.stack.setCurrentWidget(self.reports_page), self.buttons))

        if self.user_role == 'admin':
            self.users_page = UsersPage()
            self.stack.addWidget(self.users_page)
            self.buttons.append(NavButton("Пользователи", self.style().standardIcon(QStyle.SP_DirIcon),
                                          lambda: self.stack.setCurrentWidget(self.users_page), self.buttons))

        for btn in self.buttons:
            self.navbar.addWidget(btn)
        self.buttons[0].click()

        self.navbar.addStretch()
        self.apply_theme()

    def get_greeting(self):
        hour = datetime.now().hour
        if 5 <= hour < 12:
            part = "Доброе утро,\n"
        elif 12 <= hour < 17:
            part = "Добрый день,\n"
        elif 17 <= hour < 22:
            part = "Добрый вечер,\n"
        else:
            part = "Доброй ночи,"
        return f"{part} {self.username}"

    def change_language(self, lang):
        from .translations import current_language
        current_language = lang
        self.close()
        self.__init__(self.user_role, self.user_id, self.username)
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

    login_window = CombinedLoginWindow()
    if login_window.exec_() == QDialog.Accepted:
        window = MainWindow(
            user_role=login_window.role,
            user_id=login_window.user_id,
            username=login_window.user_input.text()
        )
        window.show()
        sys.exit(app.exec_())

