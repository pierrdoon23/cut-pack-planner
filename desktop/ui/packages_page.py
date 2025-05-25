from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QLineEdit, QComboBox, QCheckBox,
    QTableWidgetItem, QTabWidget
)
from .translations import tr
from ui.widgets import CommonWidgets
import requests


API_BASE = "http://localhost:8000/creation"


class PackagesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(CommonWidgets.build_header(tr('packages')))

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 10, 20, 10)
        content_layout.setSpacing(20)

        self.tabs = QTabWidget()

        self.tabs.addTab(self.build_task_tab(), "Задания")

        self.try_add_tab("base_materials", self.build_base_material_tab, "Сырьевые рулоны")
        self.try_add_tab("target_packaging", self.build_target_packaging_tab, "Целевые рулоны")
        self.try_add_tab("machines", self.build_machine_tab, "Станки")

        content_layout.addWidget(self.tabs)
        layout.addLayout(content_layout)
        layout.addWidget(CommonWidgets.build_footer())
        self.setLayout(layout)

    def build_task_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Форма добавления задания
        form_layout = QHBoxLayout()
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID рулона")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Вакуумный", "Флоу-пак", "Термоусадочный"])
        self.seam_combo = QComboBox()
        self.seam_combo.addItems(["Двойной", "Одинарный", "Ультразвук"])
        self.width_input = QLineEdit("200")
        self.length_input = QLineEdit("300")
        self.count_input = QLineEdit("100")
        self.double_cut = QCheckBox("Два потока")
        self.tape_label = QCheckBox("Наклейка")
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_task)

        for w in [self.id_input, self.type_combo, self.seam_combo,
                  self.width_input, self.length_input, self.count_input,
                  self.double_cut, self.tape_label, self.add_button]:
            form_layout.addWidget(w)

        layout.addLayout(form_layout)

        self.task_table_headers = ["ID", "Тип", "Шов", "Ширина", "Длина", "Кол-во", "2 потока", "На ленте"]
        self.task_table = QTableWidget(0, len(self.task_table_headers))
        self.task_table.setHorizontalHeaderLabels(self.task_table_headers)
        layout.addWidget(self.task_table)

        widget.setLayout(layout)
        self.fetch_data("tasks", self.task_table, self.task_table_headers)
        return widget

    def build_base_material_tab(self):
        headers = ["ID", "Название", "Длина", "Ширина", "Толщина", "Тип упаковки"]
        return self._build_simple_tab("base_materials", headers)

    def build_target_packaging_tab(self):
        headers = ["ID", "Название", "Назначение", "Длина", "Ширина", "Тип", "Шов", "2 потока"]
        return self._build_simple_tab("target_packaging", headers)

    def build_machine_tab(self):
        headers = ["ID", "Название", "Скорость", "Ширина машины"]
        return self._build_simple_tab("machines", headers)

    def _build_simple_tab(self, endpoint, headers):
        widget = QWidget()
        layout = QVBoxLayout()

        table = QTableWidget(0, len(headers))
        table.setHorizontalHeaderLabels(headers)
        layout.addWidget(table)

        refresh_btn = QPushButton("Обновить")
        refresh_btn.clicked.connect(lambda: self.fetch_data(endpoint, table, headers))
        layout.addWidget(refresh_btn)

        widget.setLayout(layout)
        self.fetch_data(endpoint, table, headers)
        return widget

    def fetch_data(self, endpoint, table, headers):
        try:
            response = requests.get(f"{API_BASE}/{endpoint}")
            response.raise_for_status()
            data = response.json()
            table.setRowCount(0)

            print(f"Данные с {endpoint}:", data)

            # Use correct keys based on the endpoint
            if endpoint == "tasks":
                data_keys = ["roll_id", "type", "seam", "width", "length", "count", "double_cut", "tape"]
            else:
                # Keep existing logic for other endpoints
                data_keys = [h.lower().replace(" ", "_") for h in headers]

            for row in data:
                row_idx = table.rowCount()
                table.insertRow(row_idx)
                for col_idx, key in enumerate(data_keys):
                    value = str(row.get(key, ""))
                    # For boolean values, display "Да" or "Нет"
                    if isinstance(row.get(key), bool):
                        value = "Да" if row.get(key) else "Нет"
                    table.setItem(row_idx, col_idx, QTableWidgetItem(value))
        except Exception as e:
            print(f"Ошибка загрузки {endpoint}: {e}")

    def add_task(self):
        data = {
            "roll_id": self.id_input.text(),
            "type": self.type_combo.currentText().lower(),
            "seam": self.seam_combo.currentText().lower(),
            "width": float(self.width_input.text()),
            "length": float(self.length_input.text()),
            "count": int(self.count_input.text()),
            "double_cut": self.double_cut.isChecked(),
            "tape": self.tape_label.isChecked(),
        }
        try:
            r = requests.post(f"{API_BASE}/tasks", json=data)
            r.raise_for_status()
            print("Задание добавлено:", data)
            self.fetch_data("tasks", self.task_table, self.task_table_headers)
        except Exception as e:
            print(f"Ошибка добавления задания: {e}")

    def try_add_tab(self, endpoint, builder, title):
        try:
            response = requests.get(f"{API_BASE}/{endpoint}")
            print(f"Проверка {title}: {response.status_code}")
            if response.status_code == 200:
                self.tabs.addTab(builder(), title)
                print(f"Вкладка добавлена: {title}")
            else:
                print(f"Endpoint {endpoint} недоступен")
        except Exception as e:
            print(f"Ошибка проверки {endpoint}: {e}")
