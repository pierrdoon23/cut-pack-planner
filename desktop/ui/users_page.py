from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QMessageBox, QScrollArea, QFrame
)
import requests

API_URL = "http://localhost:8000"


class UsersPage(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # --- Верхняя форма добавления пользователя ---
        form_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("ФИО")
        form_layout.addWidget(QLabel("ФИО:"))
        form_layout.addWidget(self.name_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        form_layout.addWidget(QLabel("Пароль:"))
        form_layout.addWidget(self.password_input)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["admin", "operator"])
        form_layout.addWidget(QLabel("Роль:"))
        form_layout.addWidget(self.role_combo)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_user)
        form_layout.addWidget(self.add_button)

        main_layout.addLayout(form_layout)

        # --- Кнопка обновления ---
        self.refresh_button = QPushButton("Обновить список")
        self.refresh_button.clicked.connect(self.load_users)
        main_layout.addWidget(self.refresh_button)

        # --- Область со скроллируемыми виджетами пользователей ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.users_container = QWidget()
        self.users_layout = QVBoxLayout()
        self.users_container.setLayout(self.users_layout)

        self.scroll_area.setWidget(self.users_container)
        main_layout.addWidget(self.scroll_area)

        self.load_users()

    def add_user(self):
        name = self.name_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText()

        if not name or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        payload = {
            "full_name": name,
            "password": password,
            "role": role
        }

        try:
            response = requests.post(f"{API_URL}/users", json=payload)
            if response.status_code == 201:
                QMessageBox.information(self, "Успешно", "Пользователь добавлен")
                self.name_input.clear()
                self.password_input.clear()
                self.load_users()
            else:
                QMessageBox.warning(self, "Ошибка", f"Не удалось добавить: {response.text}")
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Ошибка", "Сервер недоступен")

    def load_users(self):
        try:
            response = requests.get(f"{API_URL}/users")
            if response.status_code == 200:
                users = response.json()

                # Очистка предыдущих карточек
                for i in reversed(range(self.users_layout.count())):
                    widget = self.users_layout.itemAt(i).widget()
                    if widget:
                        widget.setParent(None)

                # Добавление карточек пользователей
                for user in users:
                    user_widget = self.create_user_widget(user)
                    self.users_layout.addWidget(user_widget)
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось загрузить пользователей")
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Ошибка", "Сервер недоступен")

    def create_user_widget(self, user):
        container = QFrame()
        container.setFrameShape(QFrame.Box)
        layout = QHBoxLayout(container)

        name_edit = QLineEdit(user['full_name'])
        role_combo = QComboBox()
        role_combo.addItems(["admin", "operator"])
        role_combo.setCurrentText(user['role'])

        password_edit = QLineEdit()
        password_edit.setPlaceholderText("Новый пароль")
        password_edit.setEchoMode(QLineEdit.Password)

        update_btn = QPushButton("Обновить")
        delete_btn = QPushButton("Удалить")

        # Обновление пользователя
        def update_user():
            data = {}
            new_name = name_edit.text().strip()
            new_role = role_combo.currentText()
            new_pass = password_edit.text().strip()

            if new_name != user['full_name']:
                data["full_name"] = new_name
            if new_role != user['role']:
                data["role"] = new_role
            if new_pass:
                data["password"] = new_pass

            if not data:
                return

            try:
                response = requests.patch(f"{API_URL}/users/{user['id']}", json=data)
                if response.status_code == 200:
                    QMessageBox.information(self, "Успешно", "Пользователь обновлён")
                    self.load_users()
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось обновить пользователя")
            except requests.exceptions.RequestException:
                QMessageBox.critical(self, "Ошибка", "Сервер недоступен")

        # Удаление пользователя
        def delete_user():
            confirm = QMessageBox.question(self, "Удаление",
                                           f"Удалить пользователя {user['full_name']}?",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                try:
                    response = requests.delete(f"{API_URL}/users/{user['id']}")
                    if response.status_code == 204:
                        self.load_users()
                    else:
                        QMessageBox.warning(self, "Ошибка", "Не удалось удалить пользователя")
                except requests.exceptions.RequestException:
                    QMessageBox.critical(self, "Ошибка", "Сервер недоступен")

        update_btn.clicked.connect(update_user)
        delete_btn.clicked.connect(delete_user)

        layout.addWidget(QLabel(f"ID: {user['id']}"))
        layout.addWidget(name_edit)
        layout.addWidget(role_combo)
        layout.addWidget(password_edit)
        layout.addWidget(update_btn)
        layout.addWidget(delete_btn)

        return container
