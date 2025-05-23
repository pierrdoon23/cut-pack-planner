from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox,
    QScrollArea, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ui.translations import tr
from ui.widgets import CommonWidgets
import requests


class VisualizationPage(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_base_material = None
        self.selected_target_packaging = None
        self.selected_machine = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(CommonWidgets.build_header(tr('visualization')))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 10, 20, 10)
        self.content_layout.setSpacing(20)
        self.content_layout.addLayout(self.build_content())
        self.content_layout.addStretch()
        scroll.setWidget(self.content_widget)

        layout.addWidget(scroll)
        layout.addWidget(CommonWidgets.build_footer())

    def build_content(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(15)
        vbox.setContentsMargins(10, 10, 10, 10)

        self.result_label = QLabel(tr('result'))
        self.result_label.setStyleSheet("margin-bottom: 20px; font-weight: bold; font-size: 16px;")
        vbox.addWidget(self.result_label)

        vbox.addWidget(QLabel(tr('subtitle')))

        hbox = QHBoxLayout()
        hbox.setSpacing(10)

        hbox.addWidget(QLabel(tr('src_rolls')))
        self.src_rolls_combo = QComboBox()
        self.src_rolls_combo.currentIndexChanged.connect(self.on_select_roll)
        hbox.addWidget(self.src_rolls_combo)

        hbox.addWidget(QLabel(tr('target_rolls')))
        self.target_rolls_combo = QComboBox()
        self.target_rolls_combo.currentIndexChanged.connect(self.on_select_target)
        hbox.addWidget(self.target_rolls_combo)

        hbox.addWidget(QLabel(tr('machine')))
        self.machine_combo = QComboBox()
        self.machine_combo.currentIndexChanged.connect(self.on_select_machine)
        hbox.addWidget(self.machine_combo)

        vbox.addLayout(hbox)

        create_btn = QPushButton(tr('create'))
        create_btn.setMaximumWidth(200)
        create_btn.clicked.connect(self.on_create_task)
        vbox.addWidget(create_btn)

        self.cards_container = QVBoxLayout()
        vbox.addLayout(self.cards_container)

        self.load_selection_lists()
        self.on_load_maps()

        return vbox

    def fetch_data(self, url, method="GET", json=None):
        try:
            if method == "POST":
                response = requests.post(url, json=json, timeout=2)
            else:
                response = requests.get(url, timeout=2)
            if response.status_code == 200:
                return response.json()
            print(f"Ошибка запроса: {response.status_code}")
        except Exception as e:
            print(f"Ошибка запроса: {e}")
        return []

    def load_selection_lists(self):
        self.src_rolls_combo.clear()
        self.src_materials = self.fetch_data("http://localhost:8000/tasks/base-materials")
        for mat in self.src_materials:
            self.src_rolls_combo.addItem(mat["name"], mat)

        self.target_rolls_combo.clear()
        self.target_packaging = self.fetch_data("http://localhost:8000/tasks/target-packaging")
        for pack in self.target_packaging:
            self.target_rolls_combo.addItem(pack["name"], pack)

        self.machine_combo.clear()
        self.machines = self.fetch_data("http://localhost:8000/tasks/machines")
        for machine in self.machines:
            self.machine_combo.addItem(machine["name"], machine)

    def on_select_roll(self, index):
        if index >= 0:
            self.selected_base_material = self.src_rolls_combo.itemData(index)

    def on_select_target(self, index):
        if index >= 0:
            self.selected_target_packaging = self.target_rolls_combo.itemData(index)

    def on_select_machine(self, index):
        if index >= 0:
            self.selected_machine = self.machine_combo.itemData(index)

    def on_create_task(self):
        if not all([self.selected_base_material, self.selected_target_packaging, self.selected_machine]):
            QMessageBox.warning(self, "Ошибка", "Выберите рулоны, упаковку и станок.")
            return

        payload = {
            "base_material_id": self.selected_base_material['id'],
            "target_packaging_id": self.selected_target_packaging['id'],
            "machine_id": self.selected_machine['id'],
            "user_id": 1  # фиксированный id пользователя
        }

        response = self.fetch_data("http://localhost:8000/tasks/", method="POST", json=payload)
        
        if response:
            QMessageBox.information(self, "Успех", "Задача успешно создана")
            self.on_load_maps()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось создать задачу")

    def on_load_maps(self):
        tasks = self.fetch_data("http://localhost:8000/tasks/info")
        self.clear_cards()

        for task in tasks:
            if "task_id" not in task:
                continue
            self.cards_container.addWidget(self.build_card(task))

    def clear_cards(self):
        while self.cards_container.count():
            item = self.cards_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def build_card(self, task):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: #f0f0f0;
                border-radius: 10px;
                padding: 12px;
                border: 1px solid #ccc;
            }
        """)
        layout = QVBoxLayout(card)

        def line(label, value):
            lbl = QLabel(f"<b>{label}:</b> {value}")
            lbl.setFont(QFont("Arial", 10))
            return lbl

        layout.addWidget(line("🆔 Задача ID", task.get("task_id", "N/A")))
        layout.addWidget(line("📌 Статус", task.get("status", "N/A")))
        layout.addWidget(line("📅 Начало", task.get("start_time", "N/A")))

        return card
