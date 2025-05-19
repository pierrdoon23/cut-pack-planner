from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QListWidgetItem, QListWidget,
    QScrollArea, QMessageBox, QInputDialog
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
    
        self.result_label = QLabel(tr('result'))
        self.result_label.setStyleSheet("margin-bottom: 20px; font-weight: bold;")
        vbox.addWidget(self.result_label)
    
        vbox.addWidget(QLabel(tr('subtitle')))

        hbox = QHBoxLayout()
        hbox.setSpacing(10)

        # Список исходных рулонов
        hbox.addWidget(QLabel(tr('src_rolls')))
        self.src_rolls_combo = QComboBox()
        self.src_rolls_combo.currentIndexChanged.connect(self.on_select_roll)
        hbox.addWidget(self.src_rolls_combo)

        # Список целевых упаковок
        hbox.addWidget(QLabel(tr('target_rolls')))
        self.target_rolls_list = QComboBox()
        self.src_rolls_combo.currentIndexChanged.connect(self.on_select_roll)
        hbox.addWidget(self.src_rolls_combo)

        # Список станков
        hbox.addWidget(QLabel(tr('machine')))
        self.machine_list = QComboBox()
        self.src_rolls_combo.currentIndexChanged.connect(self.on_select_roll)
        hbox.addWidget(self.src_rolls_combo)

        vbox.addLayout(hbox)

        create_btn = QPushButton(tr('create'))
        create_btn.setMaximumWidth(200)
        create_btn.clicked.connect(self.on_create_task)
        vbox.addWidget(create_btn)

        self.map_list = QListWidget()
        vbox.addWidget(self.map_list)

        self.load_selection_lists()
        self.on_load_maps()
        return vbox

    
    def on_load_maps(self):
        tasks = self.fetch_data("http://localhost:8000/cutting-maps")
        task_info = self.fetch_data("http://localhost:8000/task-info")
        machines = self.fetch_data("http://localhost:8000/machines")
        machine_map = {m['id']: m['name'] for m in machines}
        self.map_list.clear()
        info_map = {info['task_id']: info for info in task_info}
        for t in tasks:
            info = info_map.get(t['id'], {})
            status = info.get("status", "unknown")
            created = info.get("start_time", "N/A")
            machine_name = machine_map.get(t.get('machine_id'), "N/A")
        self.map_list.addItem(QListWidgetItem(f"Задача ID: {t['id']} | Статус: {status} | Станок: {machine_name} | Начато: {created}"))

    def on_select(self):
        materials = self.fetch_data("http://localhost:8000/base-materials")
        names = [m['name'] for m in materials]
        name, ok = QInputDialog.getItem(self, "Выбор материала", "Материалы:", names, 0, False)
        if ok and name:
            self.src_rolls_edit.setText(name)
            self.selected_base_material = next((m for m in materials if m['name'] == name), None)

    def on_set(self):
        targets = self.fetch_data("http://localhost:8000/target-packaging")
        names = [t['name'] for t in targets]
        name, ok = QInputDialog.getItem(self, "Выбор упаковки", "Упаковка:", names, 0, False)
        if ok and name:
            self.target_rolls_edit.setText(name)
            self.selected_target_packaging = next((t for t in targets if t['name'] == name), None)

    def on_create_task(self):
        if not all([self.selected_base_material, self.selected_target_packaging, self.selected_machine]):
            QMessageBox.warning(self, "Ошибка", "Выберите рулоны, упаковку и станок.")
            return

        payload = {
            "base_material_id": self.selected_base_material['id'],
            "target_packaging_id": self.selected_target_packaging['id'],
            "user_id": 1,
            "machine_id": self.selected_machine['id']
        }

        self.fetch_data("http://localhost:8000/create-task", method="POST", json=payload)
        self.on_load_maps()

    def on_select_machine(self):
        machines = self.fetch_data("http://localhost:8000/machines")
        names = [m['name'] for m in machines]
        name, ok = QInputDialog.getItem(self, "Выбор станка", "Станки:", names, 0, False)
        if ok and name:
            self.machine_edit.setText(name)
            self.selected_machine = next((m for m in machines if m['name'] == name), None)

    def load_selection_lists(self):
        self.selected_base_material = None
        self.selected_target_packaging = None
        self.selected_machine = None

        # Загрузка рулонов
        materials = self.fetch_data("http://localhost:8000/base-materials")
        self.src_rolls_combo.clear()
        for m in materials:
            self.src_rolls_combo.addItem(m["name"], m)
            item.setData(Qt.UserRole, m)
            self.src_rolls_list.addItem(item)

        # Загрузка упаковки
        targets = self.fetch_data("http://localhost:8000/target-packaging")
        self.target_rolls_list.clear()
        for t in targets:
            item = QListWidgetItem(t["name"])
            item.setData(Qt.UserRole, t)
            self.target_rolls_list.addItem(item)

        # Загрузка станков
        machines = self.fetch_data("http://localhost:8000/machines")
        self.machine_list.clear()
        for m in machines:
            item = QListWidgetItem(m["name"])
            item.setData(Qt.UserRole, m)
            self.machine_list.addItem(item)

    def on_select_roll(self):
        item = self.src_rolls_list.currentItem()
        if item:
            self.selected_base_material = item.data(Qt.UserRole)

    def on_select_roll(self):
        index = self.src_rolls_combo.currentIndex()
        if index >= 0:
            self.selected_base_material = self.src_rolls_combo.itemData(index)


    def on_select_target(self):
        item = self.target_rolls_list.currentItem()
        if item:
            self.selected_target_packaging = item.data(Qt.UserRole)

    def on_select_machine(self):
        item = self.machine_list.currentItem()
        if item:
            self.selected_machine = item.data(Qt.UserRole)

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
        return []