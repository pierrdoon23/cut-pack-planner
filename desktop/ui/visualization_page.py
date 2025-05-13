from PyQt5.QtWidgets import ( QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QFrame )
from .translations import tr

class VisualizationPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(self.build_header())
        layout.addLayout(self.build_content())
        layout.addWidget(self.build_footer())

    def build_header(self):
        header = QFrame()
        header.setObjectName("Header")
        header.setLayout(QHBoxLayout())
        label = QLabel(tr('visualization'))
        label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        header.layout().addWidget(label)
        return header

    def build_footer(self):
        footer = QFrame()
        footer.setObjectName("Footer")
        footer.setLayout(QHBoxLayout())
        footer.layout().addWidget(QLabel("Footer content here"))
        return footer

    def build_content(self):
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel(tr('subtitle')))
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(tr('src_rolls')))
        hbox.addWidget(QLineEdit("0"))
        hbox.addWidget(QPushButton(tr('select')))
        hbox.addWidget(QLabel(tr('target_rolls')))
        hbox.addWidget(QLineEdit("3"))
        hbox.addWidget(QPushButton(tr('set')))
        hbox.addWidget(QPushButton(tr('params')))
        vbox.addLayout(hbox)

        btn_layout = QHBoxLayout()
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