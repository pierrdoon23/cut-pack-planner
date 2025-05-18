from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
)
from ui.translations import tr
from ui.widgets import CommonWidgets
import requests

class VisualizationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.result_label = None
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
        self.src_rolls_edit = QLineEdit("0")
        hbox.addWidget(self.src_rolls_edit)
        select_btn = QPushButton(tr('select'))
        select_btn.clicked.connect(self.on_select)
        hbox.addWidget(select_btn)

        hbox.addWidget(QLabel(tr('target_rolls')))
        self.target_rolls_edit = QLineEdit("3")
        hbox.addWidget(self.target_rolls_edit)
        set_btn = QPushButton(tr('set'))
        set_btn.clicked.connect(self.on_set)
        hbox.addWidget(set_btn)
        params_btn = QPushButton(tr('params'))
        params_btn.clicked.connect(self.on_params)
        hbox.addWidget(params_btn)

        vbox.addLayout(hbox)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        btn_layout.addWidget(QPushButton(tr('new_map')))
        btn_layout.addWidget(QPushButton(tr('export')))

        optimize_btn = QPushButton(tr('optimize'))
        optimize_btn.setStyleSheet("background-color: #007bff; color: white;")
        optimize_btn.clicked.connect(self.on_optimize)
        btn_layout.addWidget(optimize_btn)

        vbox.addLayout(btn_layout)

        self.result_label = QLabel(tr('result'))
        self.result_label.setStyleSheet("margin-top: 20px; font-weight: bold;")
        vbox.addWidget(self.result_label)

        return vbox

    def on_select(self):
        data = self.fetch_data("http://localhost:8000/")


    def on_set(self):
        data = self.fetch_data("http://localhost:8000/")


    def on_params(self):
        data = self.fetch_data("http://localhost:8000/")


    def on_optimize(self):
        data = self.fetch_data("http://localhost:8000/")


    def fetch_data(self, url):
        try:
            response = requests.get(url, timeout=1.5)
            if response.status_code == 200:
                return response.json()
            else:
                return {}
        except Exception as e:
            print(f"Ошибка запроса: {url}", e)
            return {}
