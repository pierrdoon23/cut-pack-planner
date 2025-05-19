from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem,
    QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt
from ui.translations import tr
from ui.widgets import CommonWidgets
import requests

class VisualizationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.result_label = None
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(CommonWidgets.build_header(tr('visualization')))

        # Контент на всю ширину
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 10, 20, 10)
        content_layout.setSpacing(20)
        content_layout.addLayout(self.build_content())
        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

        layout.addWidget(CommonWidgets.build_footer())

    def build_content(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(15)
        vbox.setContentsMargins(10, 10, 10, 10)
        
        # Add result label at the top
        self.result_label = QLabel(tr('result'))
        self.result_label.setStyleSheet("margin-bottom: 20px; font-weight: bold;")
        vbox.addWidget(self.result_label)
        
        vbox.addWidget(QLabel(tr('subtitle')))

        hbox = QHBoxLayout()
        hbox.setSpacing(10)

        hbox.addWidget(QLabel(tr('src_rolls')))
        self.src_rolls_edit = QLineEdit("0")
        self.src_rolls_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.src_rolls_edit.setMaximumWidth(200)
        hbox.addWidget(self.src_rolls_edit)
        select_btn = QPushButton(tr('select'))
        select_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        select_btn.clicked.connect(self.on_select)
        select_btn.setMaximumWidth(200)
        hbox.addWidget(select_btn)

        hbox.addWidget(QLabel(tr('target_rolls')))
        self.target_rolls_edit = QLineEdit("3")
        self.target_rolls_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.target_rolls_edit.setMaximumWidth(200)
        hbox.addWidget(self.target_rolls_edit)
        set_btn = QPushButton(tr('set'))
        set_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        set_btn.clicked.connect(self.on_set)
        set_btn.setMaximumWidth(200)
        hbox.addWidget(set_btn)
        params_btn = QPushButton(tr('params'))
        params_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        params_btn.clicked.connect(self.on_params)
        params_btn.setMaximumWidth(200)
        hbox.addWidget(params_btn)

        vbox.addLayout(hbox)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        for btn in [QPushButton(tr('new_map')), QPushButton(tr('export'))]:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMaximumWidth(200)
            btn_layout.addWidget(btn)

        optimize_btn = QPushButton(tr('optimize'))
        optimize_btn.setStyleSheet("background-color: #007bff; color: white;")
        optimize_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        optimize_btn.clicked.connect(self.on_optimize)
        optimize_btn.setMaximumWidth(200)
        btn_layout.addWidget(optimize_btn)
        btn_layout.addStretch()

        vbox.addLayout(btn_layout)

        # Create scrollable list widget
        list_container = QWidget()
        list_layout = QVBoxLayout(list_container)
        
        self.map_list = QListWidget()
        self.map_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.map_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        list_layout.addWidget(self.map_list)
        
        load_maps_btn = QPushButton(tr('load_maps'))
        load_maps_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        load_maps_btn.clicked.connect(self.on_load_maps)
        load_maps_btn.setMaximumWidth(400)
        list_layout.addWidget(load_maps_btn)
        
        vbox.addWidget(list_container)
        vbox.addStretch()

        return vbox
    
    def on_load_maps(self):
        maps = self.fetch_data("http://localhost:8000/cutting-maps")
        self.map_list.clear()
        for m in maps:
            item_text = f"ID: {m['id']} | Время: {m['created_at']}"
            self.map_list.addItem(QListWidgetItem(item_text))

    def on_select(self):
        data = self.fetch_data("http://localhost:8000/select", method="POST", json={
            "length": int(self.src_rolls_edit.text()),
            "type": "source"
        })

    def on_set(self):
        data = self.fetch_data("http://localhost:8000/set", method="POST", json={
            "length": int(self.target_rolls_edit.text()),
            "type": "target"
        })

    def on_params(self):
        data = self.fetch_data("http://localhost:8000/params")
        print("Параметры:", data)

    def on_optimize(self):
        data = self.fetch_data("http://localhost:8000/optimize")
        self.result_label.setText(
            f"Результаты оптимизации\nЭффективность: {data.get('efficiency', 0)}%, Отходы: {data.get('waste', 0)} мм"
        )

    def fetch_data(self, url, method="GET", json=None):
        try:
            if method == "POST":
                response = requests.post(url, json=json, timeout=1.5)
            else:
                response = requests.get(url, timeout=1.5)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка запроса: {response.status_code}")
        except Exception as e:
            print(f"Сервер недоступен: {e}")
        return {}