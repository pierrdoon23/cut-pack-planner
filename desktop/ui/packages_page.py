from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit,
    QComboBox, QCheckBox, QTabWidget, QLabel, QGroupBox, QMessageBox, 
    QScrollArea
)
from .translations import tr
from ui.widgets import CommonWidgets
import requests
from functools import partial


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

        self.try_add_tab("base_materials", self.build_base_material_tab, "Сырьевые рулоны")
        self.try_add_tab("target_packaging", self.build_target_packaging_tab, "Целевые рулоны")
        self.try_add_tab("machines", self.build_machine_tab, "Станки")

        content_layout.addWidget(self.tabs)
        layout.addLayout(content_layout)
        layout.addWidget(CommonWidgets.build_footer())
        self.setLayout(layout)

    def build_base_material_tab(self):
        headers = ["ID", "Название", "Длина", "Ширина", "Толщина", "Тип упаковки"]
        keys = ["id", "name", "length", "width", "thickness", "package_type"]

        form_fields = {
            "name": QLineEdit(),
            "length": QLineEdit(),
            "width": QLineEdit(),
            "thickness": QLineEdit(),
            "package_type": QComboBox()
        }

        self.package_type_mapping = {
            "Вакуумный": "vacuum",
            "Флоу-пак": "flow_pack",
            "Термоусадочный": "shrink"
        }
        for label in self.package_type_mapping:
            form_fields["package_type"].addItem(label)

        return self._build_tab("base_materials", headers, keys, form_fields)

    def build_target_packaging_tab(self):
        headers = ["ID", "Название", "Назначение", "Длина", "Ширина", "Тип", "Шов", "2 потока"]
        keys = ["id", "name", "purpose", "length", "width", "package_type", "seam_type", "is_two_streams"]

        form_fields = {
            "name": QLineEdit(),
            "purpose": QLineEdit(),
            "length": QLineEdit(),
            "width": QLineEdit(),
            "package_type": QComboBox(),
            "seam_type": QComboBox(),
            "is_two_streams": QCheckBox("Два потока")
        }

        self.package_type_mapping = {
            "Вакуумный": "vacuum",
            "Флоу-пак": "flow_pack",
            "Термоусадочный": "shrink"
        }
        for label in self.package_type_mapping:
            form_fields["package_type"].addItem(label)

        self.seam_mapping = {
            "Двойной": "double_seam",
            "Одинарный": "single_seam",
            "Ультразвук": "ultrasonic"
        }
        for label in self.seam_mapping:
            form_fields["seam_type"].addItem(label)

        return self._build_tab("target_packaging", headers, keys, form_fields)

    def build_machine_tab(self):
        headers = ["ID", "Название", "Скорость", "Ширина машины"]
        keys = ["id", "name", "cutting_speed", "machine_width"]

        form_fields = {
            "name": QLineEdit(),
            "cutting_speed": QLineEdit(),
            "machine_width": QLineEdit()
        }

        return self._build_tab("machines", headers, keys, form_fields)

    def _build_tab(self, endpoint, headers, data_keys, form_fields):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        inner_widget = QWidget()
        layout = QVBoxLayout(inner_widget)

        # ======= 1. ФОРМА ДОБАВЛЕНИЯ =======
        form_layout = QHBoxLayout()
        for key, field in form_fields.items():
            if isinstance(field, QCheckBox):
                checkbox_layout = QVBoxLayout()
                checkbox_layout.addWidget(field)
                form_layout.addLayout(checkbox_layout)
            else:
                form_layout.addWidget(field)

        add_btn = QPushButton("Добавить")
        form_layout.addWidget(add_btn)
        layout.addLayout(form_layout)

        # ======= 2. КНОПКА ОБНОВЛЕНИЯ =======
        refresh_btn = QPushButton("Обновить")
        layout.addWidget(refresh_btn)

        # ======= 3. КОНТЕЙНЕР С ДАННЫМИ =======
        records_container = QVBoxLayout()
        layout.addLayout(records_container)

        def on_add():
            data = {}
            for key, field in form_fields.items():
                if isinstance(field, QLineEdit):
                    val = field.text()
                    try:
                        val = float(val) if '.' in val else int(val)
                    except ValueError:
                        val = val.strip()
                elif isinstance(field, QComboBox):
                    selected = field.currentText()
                    if key == "package_type":
                        val = self.package_type_mapping.get(selected, "")
                    elif key == "seam_type":
                        val = self.seam_mapping.get(selected, "")
                    else:
                        val = selected.lower()
                elif isinstance(field, QCheckBox):
                    val = field.isChecked()
                else:
                    val = None
                data[key] = val

            try:
                response = requests.post(f"{API_BASE}/{endpoint}", json=data)
                response.raise_for_status()
                self.fetch_data(endpoint, records_container, data_keys)
            except Exception as e:
                print(f"Ошибка добавления: {e}")
                QMessageBox.warning(self, "Ошибка", f"Не удалось добавить запись: {e}")

        add_btn.clicked.connect(on_add)

        refresh_btn = QPushButton("Обновить")
        refresh_btn.clicked.connect(lambda: self.fetch_data(endpoint, records_container, data_keys))
        layout.addWidget(refresh_btn)

        scroll.setWidget(inner_widget)
        self.fetch_data(endpoint, records_container, data_keys)
        return scroll


    def fetch_data(self, endpoint, container, data_keys):
        try:
            response = requests.get(f"{API_BASE}/{endpoint}")
            response.raise_for_status()
            data = response.json()

            while container.count():
                child = container.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            for row in data:
                group = QGroupBox()
                box_layout = QVBoxLayout()

                for key in data_keys:
                    value = row.get(key, "")
                    if isinstance(value, bool):
                        value = "Да" if value else "Нет"
                    box_layout.addWidget(QLabel(f"<b>{key}</b>: {value}"))

                delete_btn = QPushButton("Удалить")
                delete_btn.clicked.connect(partial(self.delete_entry, endpoint, row["id"], container, data_keys))
                box_layout.addWidget(delete_btn)

                group.setLayout(box_layout)
                container.addWidget(group)

        except Exception as e:
            print(f"Ошибка загрузки {endpoint}: {e}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные: {e}")

    def delete_entry(self, endpoint, record_id, container, data_keys):
        try:
            response = requests.delete(f"{API_BASE}/{endpoint}/{record_id}")
            response.raise_for_status()
            self.fetch_data(endpoint, container, data_keys)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                error_msg = e.response.json().get('detail', 'Неизвестная ошибка')
                QMessageBox.warning(self, "Ошибка", error_msg)
            elif e.response.status_code == 404:
                QMessageBox.warning(self, "Ошибка", "Запись не найдена")
            else:
                QMessageBox.warning(self, "Ошибка", f"Не удалось удалить запись: {e}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить запись: {e}")

    def try_add_tab(self, endpoint, builder, title):
        try:
            response = requests.get(f"{API_BASE}/{endpoint}")
            if response.status_code == 200:
                self.tabs.addTab(builder(), title)
            else:
                print(f"Endpoint {endpoint} недоступен")
        except Exception as e:
            print(f"Ошибка проверки {endpoint}: {e}")
