import requests
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

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
        self.token = None  # Если будет использоваться JWT

    def handle_login(self):
        username = self.user_input.text()
        password = self.password_input.text()
        print(username, password)

        try:
            response = requests.post("http://localhost:8000/users/login", json={
                "username": username,
                "password": password
            })

            if response.status_code == 200:
                data = response.json()
                self.role = data.get("role")
                self.user_id = data.get("id")
                self.token = data.get("token")  # Если используется
                self.accept()
            else:
                QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль.")
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Сервер недоступен", "Не удалось подключиться к серверу.")
