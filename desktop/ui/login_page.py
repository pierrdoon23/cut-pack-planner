import requests
from PyQt5.QtWidgets import (
    QDialog, QHBoxLayout, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QWidget
)
from PyQt5.QtCore import Qt


class CombinedLoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Подключение и вход")
        self.setFixedSize(800, 400)

        main_layout = QHBoxLayout()

        # Левая часть — подключение
        connection_widget = QWidget()
        connection_layout = QVBoxLayout()

        # Настройки сервера
        server_group = QVBoxLayout()
        server_group.addWidget(QLabel("Настройки сервера:"))
        
        self.api_input = QLineEdit("http://localhost")
        self.api_input.setPlaceholderText("URL сервера")
        server_group.addWidget(QLabel("Адрес сервера:"))
        server_group.addWidget(self.api_input)

        self.port_input = QLineEdit("8000")
        self.port_input.setPlaceholderText("Порт")
        server_group.addWidget(QLabel("Порт:"))
        server_group.addWidget(self.port_input)

        self.ping_button = QPushButton("Проверить соединение")
        self.ping_button.clicked.connect(self.check_connection)
        server_group.addWidget(self.ping_button)

        connection_layout.addLayout(server_group)
        connection_widget.setLayout(connection_layout)
        main_layout.addWidget(connection_widget)

        # Правая часть — логин
        login_widget = QWidget()
        login_layout = QVBoxLayout()

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Имя пользователя")
        login_layout.addWidget(QLabel("Имя пользователя:"))
        login_layout.addWidget(self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        login_layout.addWidget(QLabel("Пароль:"))
        login_layout.addWidget(self.password_input)

        self.login_button = QPushButton("Войти")
        self.login_button.setEnabled(False)
        self.login_button.clicked.connect(self.handle_login)
        login_layout.addWidget(self.login_button)

        login_widget.setLayout(login_layout)
        main_layout.addWidget(login_widget)

        self.setLayout(main_layout)

        # Параметры
        self.base_url = ""
        self.role = None
        self.user_id = None
        self.token = None

    def check_connection(self):
        api_url = self.api_input.text().strip()
        port = self.port_input.text().strip()
        self.base_url = f"{api_url}:{port}"

        try:
            response = requests.get(f"{self.base_url}/users/ping")
            if response.status_code == 200:
                QMessageBox.information(self, "Успех", "Соединение с сервером установлено.")
                self.login_button.setEnabled(True)
            else:
                QMessageBox.warning(self, "Ошибка", "Сервер ответил, но с ошибкой.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Ошибка подключения", f"Не удалось подключиться к серверу:\n{str(e)}")
            self.login_button.setEnabled(False)

    def handle_login(self):
        username = self.user_input.text()
        password = self.password_input.text()

        try:
            response = requests.post(f"{self.base_url}/users/login", json={
                "username": username,
                "password": password
            })

            if response.status_code == 200:
                data = response.json()
                self.role = data.get("role")
                self.user_id = data.get("id")
                self.token = data.get("token")
                QMessageBox.information(self, "Успех", "Вы вошли в систему.")
                self.accept()
            else:
                QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Сервер недоступен", f"Не удалось подключиться к серверу.\n\n{str(e)}")
