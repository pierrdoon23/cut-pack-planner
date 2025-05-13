from PyQt5.QtWidgets import ( QWidget, QVBoxLayout, QLineEdit, QComboBox, QFormLayout )
from ui.translations import tr
from ui.widgets import CommonWidgets

class SettingsPage(QWidget):
    def __init__(self, change_language, change_theme):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(CommonWidgets.build_header(tr('settings')))

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
        layout.addWidget(CommonWidgets.build_footer())