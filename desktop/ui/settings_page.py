from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QComboBox, QFormLayout,
    QSizePolicy, QPushButton, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import QSettings
from ui.translations import tr
from ui.widgets import CommonWidgets


class SettingsPage(QWidget):
    def __init__(self, change_language, change_theme, logout_callback):
        super().__init__()
        self.change_language = change_language
        self.change_theme = change_theme
        self.logout_callback = logout_callback

        self.settings = QSettings("MyCompany", "MyApp")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(CommonWidgets.build_header(tr('settings')))

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(40, 20, 40, 20)
        content_layout.setSpacing(30)

        form = QFormLayout()
        form.setSpacing(20)

        self.lang_combo = QComboBox()
        self.lang_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.lang_combo.addItems(['ru', 'en'])
        self.lang_combo.setMaximumWidth(400)
        self.lang_combo.setCurrentText(self.settings.value("ui/language", "ru"))
        self.lang_combo.currentTextChanged.connect(self.on_language_changed)
        form.addRow(tr('language'), self.lang_combo)

        self.theme_combo = QComboBox()
        self.theme_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.theme_combo.addItems(['light', 'dark'])
        self.theme_combo.setMaximumWidth(400)
        self.theme_combo.setCurrentText(self.settings.value("ui/theme", "light"))
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        form.addRow(tr('theme'), self.theme_combo)

        content_layout.addLayout(form)

        # Кнопка выхода из аккаунта
        logout_button = QPushButton(tr("logout"))
        logout_button.setStyleSheet("padding: 10px;")
        logout_button.clicked.connect(self.logout)

        # Кнопка очистки всех данных
        clear_button = QPushButton(tr("clear_data"))
        clear_button.setStyleSheet("padding: 10px; background-color: #d9534f; color: white;")
        clear_button.clicked.connect(self.clear_settings)

        content_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        content_layout.addWidget(logout_button)
        content_layout.addWidget(clear_button)

        layout.addLayout(content_layout)
        layout.addWidget(CommonWidgets.build_footer())

    def on_language_changed(self, lang_code):
        self.settings.setValue("ui/language", lang_code)
        self.change_language(lang_code)

    def on_theme_changed(self, theme):
        self.settings.setValue("ui/theme", theme)
        self.change_theme(theme)

    def logout(self):
        confirm = QMessageBox.question(
            self,
            tr("confirm_logout"),
            tr("are_you_sure_logout"),
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.logout_callback()

    def clear_settings(self):
        confirm = QMessageBox.question(
            self,
            tr("confirm_clear_data"),
            tr("are_you_sure_clear_data"),
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.settings.clear()
            QMessageBox.information(self, tr("data_cleared"), tr("all_data_cleared"))
