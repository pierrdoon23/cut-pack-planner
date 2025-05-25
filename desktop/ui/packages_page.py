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

        self.type_mapping = {
            "Вакуумный": "vacuum",
            "Флоу-пак": "flow_pack",
            "Термоусадочный": "shrink"
        }
        # Добавляем типы упаковки
        for label in self.type_mapping:
            form_fields["package_type"].addItem(label)

        self.seam_mapping = {
            "Двойной": "double_seam",
            "Одинарный": "single_seam",
            "Ультразвук": "ultrasonic"
        }
        # Добавляем типы швов
        for label in self.seam_mapping:
            form_fields["seam_type"].addItem(label)

        return self._build_tab("target_packaging", headers, keys, form_fields)


    def build_machine_tab(self):
        headers = ["ID", "Название", "Скорость", "Ширина машины"]
        keys = ["id", "name", "cutting_speed", "machine_width"]

        form_fields = {
            "name": QLineEdit(),
            "speed": QLineEdit(),
            "machine_width": QLineEdit()
        }

        return self._build_tab("machines", headers, keys, form_fields)

    def _build_tab(self, endpoint, headers, data_keys, form_fields):
        widget = QWidget()
        layout = QVBoxLayout()

        table = QTableWidget(0, len(headers))
        table.setHorizontalHeaderLabels(headers)
        layout.addWidget(table)

        form_layout = QHBoxLayout()
        for field in form_fields.values():
            form_layout.addWidget(field)
        add_btn = QPushButton("Добавить")
        form_layout.addWidget(add_btn)
        layout.addLayout(form_layout)

        def on_add():
            data = {}

            for key, widget in form_fields.items():
                if isinstance(widget, QLineEdit):
                    val = widget.text()
                    try:
                        val = float(val) if '.' in val else int(val)
                    except ValueError:
                        val = val.strip()

                elif isinstance(widget, QComboBox):
                    selected = widget.currentText()
                    if key in ["package_type", "type"]:
                        val = self.package_type_mapping.get(selected, "")
                    elif key == "seam":
                        val = self.seam_mapping.get(selected, "")
                    else:
                        val = selected.lower()

                elif isinstance(widget, QCheckBox):
                    val = widget.isChecked()

                else:
                    val = None

                # Ключи, которые должны быть переименованы под API
                if key == "type":
                    data["package_type"] = val
                elif key == "seam":
                    data["seam_type"] = val
                elif key == "double_cut":
                    data["is_two_streams"] = val
                elif key == "speed":
                    data["cutting_speed"] = val
                else:
                    data[key] = val

            try:
                # Преобразуем значения enum в правильный формат
                if 'package_type' in data:
                    data['package_type'] = data['package_type'].lower()
                if 'seam_type' in data:
                    data['seam_type'] = data['seam_type'].lower()

                response = requests.post(f"{API_BASE}/{endpoint}", json=data)
                response.raise_for_status()
                print(f"Добавлено в {endpoint}: {data}")
                self.fetch_data(endpoint, table, data_keys)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 400:
                    error_msg = e.response.json().get('detail', 'Неизвестная ошибка')
                    print(f"Ошибка добавления в {endpoint}: {error_msg}")
                elif e.response.status_code == 422:
                    error_data = e.response.json()
                    if isinstance(error_data.get('detail'), list):
                        error_msg = "Ошибка валидации данных:\n"
                        for error in error_data['detail']:
                            error_msg += f"{error.get('loc', [''])[-1]}: {error.get('msg', '')}\n"
                    else:
                        error_msg = str(error_data)
                    print(f"Ошибка добавления в {endpoint}: {error_msg}")
                else:
                    print(f"Ошибка добавления в {endpoint}: {e}")
            except Exception as e:
                print(f"Ошибка добавления в {endpoint}: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    print("Ответ сервера:", e.response.text)

        add_btn.clicked.connect(on_add)

        refresh_btn = QPushButton("Обновить")
        refresh_btn.clicked.connect(lambda: self.fetch_data(endpoint, table, data_keys))
        layout.addWidget(refresh_btn)

        widget.setLayout(layout)
        self.fetch_data(endpoint, table, data_keys)
        return widget


    def fetch_data(self, endpoint, table, data_keys):
        try:
            response = requests.get(f"{API_BASE}/{endpoint}")
            response.raise_for_status()
            data = response.json()
            table.setRowCount(0)

            for row in data:
                row_idx = table.rowCount()
                table.insertRow(row_idx)
                for col_idx, key in enumerate(data_keys):
                    value = row.get(key, "")
                    if isinstance(value, bool):
                        value = "Да" if value else "Нет"
                    table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        except Exception as e:
            print(f"Ошибка загрузки {endpoint}: {e}")

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
