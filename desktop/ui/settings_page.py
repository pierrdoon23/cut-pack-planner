from PyQt5.QtWidgets import ( QWidget, QVBoxLayout, QLineEdit, QComboBox, QFormLayout, QSizePolicy, QHBoxLayout )
from ui.translations import tr
from ui.widgets import CommonWidgets

class SettingsPage(QWidget):
    def __init__(self, change_language, change_theme):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(CommonWidgets.build_header(tr('settings')))
        # Контент на всю ширину
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 10, 20, 10)
        content_layout.setSpacing(20)
        form = QFormLayout()
        self.lang_combo = QComboBox()
        self.lang_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.lang_combo.addItems(['ru', 'en'])
        self.lang_combo.currentTextChanged.connect(change_language)
        self.lang_combo.setMaximumWidth(300)
        form.addRow(tr('language'), self.lang_combo)

        self.theme_combo = QComboBox()
        self.theme_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.theme_combo.addItems(['light', 'dark'])
        self.theme_combo.currentTextChanged.connect(change_theme)
        self.theme_combo.setMaximumWidth(300)
        form.addRow(tr('theme'), self.theme_combo)

        self.api_url_input = QLineEdit("http://localhost")
        self.api_url_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.api_url_input.setMaximumWidth(300)
        form.addRow(tr('api_url'), self.api_url_input)

        self.port_input = QLineEdit("8000")
        self.port_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.port_input.setMaximumWidth(300)
        form.addRow(tr('port'), self.port_input)

        content_layout.addLayout(form)
        content_layout.addStretch()
        layout.addLayout(content_layout)
        layout.addWidget(CommonWidgets.build_footer())