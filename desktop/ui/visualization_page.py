from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
)
from ui.translations import tr
from ui.widgets import CommonWidgets

class VisualizationPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.addWidget(CommonWidgets.build_header(tr('visualization')))
        layout.addLayout(self.build_content())
        layout.addStretch()
        layout.addWidget(CommonWidgets.build_footer())

    def build_content(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(15)
        vbox.setContentsMargins(10, 10, 10, 10)
        vbox.addWidget(QLabel(tr('subtitle')))

        hbox = QHBoxLayout()
        hbox.setSpacing(10)

        hbox.addWidget(QLabel(tr('src_rolls')))
        hbox.addWidget(QLineEdit("0"))
        hbox.addWidget(QPushButton(tr('select')))

        hbox.addWidget(QLabel(tr('target_rolls')))
        hbox.addWidget(QLineEdit("3"))
        hbox.addWidget(QPushButton(tr('set')))
        hbox.addWidget(QPushButton(tr('params')))

        vbox.addLayout(hbox)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

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
