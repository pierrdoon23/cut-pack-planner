import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QLineEdit, QDialog, QDialogButtonBox,
    QMainWindow, QStackedWidget, QHBoxLayout, QFrame,
    QStyle, QStyleFactory
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.setFixedSize(300, 180)
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Имя пользователя")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(QLabel("Пожалуйста, войдите:"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def get_credentials(self):
        return self.username_input.text(), self.password_input.text()


class AddTextDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить текст")
        self.setModal(True)

        layout = QVBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите текст...")

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(self.input_field)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_text(self):
        return self.input_field.text()


class MainPage(QWidget):
    def __init__(self, add_text_callback):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Кнопка справа вверху
        top_row = QHBoxLayout()
        top_row.addStretch()
        self.add_widget_button = QPushButton("+")
        self.add_widget_button.setFixedSize(30, 30)
        self.add_widget_button.clicked.connect(add_text_callback)
        top_row.addWidget(self.add_widget_button)

        layout.addLayout(top_row)

        # Виджеты будут добавляться сверху вниз
        self.dynamic_area_container = QWidget()
        self.dynamic_area = QVBoxLayout()
        self.dynamic_area.setAlignment(Qt.AlignTop)  # ⬅️ Важно!
        self.dynamic_area_container.setLayout(self.dynamic_area)

        layout.addWidget(self.dynamic_area_container)
        self.setLayout(layout)

    def add_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("padding: 5px; background-color: #ecf0f1; border: 1px solid #ccc;")
        self.dynamic_area.addWidget(label)



class StatsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = QLabel("📊 Статистика")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 18px;")
        self.layout.addWidget(self.title)

        self.canvas = None
        self.update_chart()

    def update_chart(self):
        # Удалить старый график
        if self.canvas:
            self.layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

        try:
            with open("desktop/data.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            self.canvas = self.create_chart(data)
            self.layout.addWidget(self.canvas)

        except Exception as e:
            error_label = QLabel(f"Ошибка загрузки графика: {e}")
            error_label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(error_label)

    def create_chart(self, data):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(data["labels"], data["values"], color="#3498db")
        ax.set_title(data.get("title", "Статистика"))
        ax.set_ylabel("Количество")
        canvas = FigureCanvas(fig)
        return canvas


class GreetingPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("👋 Привет!")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)


class NavButton(QPushButton):
    def __init__(self, text, icon, callback):
        super().__init__(text)
        self.setIcon(icon)
        self.clicked.connect(callback)
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 5px 15px;
                background-color: #34495e;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #3d566e;
            }
        """)


class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username

        self.setWindowTitle("Приложение с Навигацией")
        self.setMinimumSize(1024, 768)

        # Центр. виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # ===== Хедер =====
        header = QLabel("🔷 Моё Приложение")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("background-color: #2c3e50; color: white; padding: 10px; font-size: 18pt;")
        main_layout.addWidget(header)

        # ===== Контент =====
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout, 1)

        # ===== Навбар =====
        navbar_frame = QFrame()
        navbar_frame.setStyleSheet("background-color: #2c3e50;")
        navbar_layout = QVBoxLayout(navbar_frame)

        # Имя пользователя
        user_label = QLabel(f"👤 {self.username}")
        user_label.setStyleSheet("color: white; font-weight: bold; padding: 10px;")
        navbar_layout.addWidget(user_label)

        # Кнопки навигации
        icon_home = self.style().standardIcon(QStyle.SP_DesktopIcon)
        icon_greet = self.style().standardIcon(QStyle.SP_DialogYesButton)
        icon_stats = self.style().standardIcon(QStyle.SP_FileDialogDetailedView)

        home_btn = NavButton("Главная", icon_home, self.show_main_page)
        greet_btn = NavButton("Приветствие", icon_greet, self.show_greeting_page)
        stats_btn = NavButton("Статистика", icon_stats, self.show_stats_page)

        navbar_layout.addWidget(home_btn)
        navbar_layout.addWidget(greet_btn)
        navbar_layout.addWidget(stats_btn)
        navbar_layout.addStretch()

        content_layout.addWidget(navbar_frame, 1)

        # ===== Страницы (stack) =====
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack, 4)

        self.main_page = MainPage(self.open_add_text_dialog)
        self.greeting_page = GreetingPage()
        self.stats_page = StatsPage()

        self.stack.addWidget(self.main_page)
        self.stack.addWidget(self.greeting_page)
        self.stack.addWidget(self.stats_page)

        self.stack.setCurrentWidget(self.main_page)

        # ===== Футер =====
        footer = QLabel("© 2025 Моё Приложение")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("background-color: #ecf0f1; color: #2c3e50; padding: 5px;")
        main_layout.addWidget(footer)

    def open_add_text_dialog(self):
        dialog = AddTextDialog()
        if dialog.exec_() == QDialog.Accepted:
            text = dialog.get_text().strip()
            if text:
                self.main_page.add_label(text)

    def show_main_page(self):
        self.stack.setCurrentWidget(self.main_page)

    def show_greeting_page(self):
        self.stack.setCurrentWidget(self.greeting_page)

    def show_stats_page(self):
        self.stats_page.update_chart()  # 🔄 Обновляем перед показом
        self.stack.setCurrentWidget(self.stats_page)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create("Fusion"))

    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        username, _ = login.get_credentials()
        window = MainWindow(username=username or "Гость")
        window.show()
        window.setWindowState(Qt.WindowMaximized)
        sys.exit(app.exec_())
