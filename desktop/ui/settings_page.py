from PyQt5.QtWidgets import ( QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QFormLayout, QFrame )
from .translations import tr

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