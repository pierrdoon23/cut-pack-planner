import json
from PyQt5.QtWidgets import ( QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QLineEdit, QComboBox, QSizePolicy, QCheckBox, QTableWidgetItem )
from .translations import tr

class PackagesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # ----- Форма добавления -----
        form_layout = QHBoxLayout()

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Введите ID рулона")

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Стандартный", "Вакуумный"])

        self.seam_combo = QComboBox()
        self.seam_combo.addItems(["Прямой", "Полукруглый (R50)"])

        self.width_input = QLineEdit("200")
        self.length_input = QLineEdit("300")
        self.count_input = QLineEdit("100")

        self.double_cut = QCheckBox("Нарезка в два потока")
        self.tape_label = QCheckBox("Наклейка на ленту")

        self.add_button = QPushButton("Добавить задание")
        self.add_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        form_layout.addWidget(QLabel("ID рулона:"))
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(QLabel("Тип пакета:"))
        form_layout.addWidget(self.type_combo)
        form_layout.addWidget(QLabel("Тип шва:"))
        form_layout.addWidget(self.seam_combo)
        form_layout.addWidget(QLabel("Ширина:"))
        form_layout.addWidget(self.width_input)
        form_layout.addWidget(QLabel("Длина:"))
        form_layout.addWidget(self.length_input)
        form_layout.addWidget(QLabel("Кол-во:"))
        form_layout.addWidget(self.count_input)
        form_layout.addWidget(self.double_cut)
        form_layout.addWidget(self.tape_label)
        form_layout.addWidget(self.add_button)

        layout.addLayout(form_layout)

        # ----- Таблица заданий -----
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID рулона", "Тип пакета", "Тип шва",
            "Размеры (мм)", "Количество", "Два потока",
            "На ленте", ""
        ])
        layout.addWidget(QLabel("\nСписок заданий на нарезку пакетов"))
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.load_data()

    def load_data(self):
        try:
            with open("desktop/data2.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            self.table.setRowCount(len(data))
            for row, task in enumerate(data):
                self.table.setItem(row, 0, QTableWidgetItem(task["id"]))
                self.table.setItem(row, 1, QTableWidgetItem(task["type"]))
                self.table.setItem(row, 2, QTableWidgetItem(task["seam"]))

                size_str = f"{task['width']} x {task['height']}"
                self.table.setItem(row, 3, QTableWidgetItem(size_str))

                self.table.setItem(row, 4, QTableWidgetItem(str(task["count"])))

                self.table.setItem(row, 5, QTableWidgetItem("✓" if task["double"] else "—"))
                self.table.setItem(row, 6, QTableWidgetItem("✓" if task["tape"] else "—"))

                self.table.setItem(row, 7, QTableWidgetItem("🗑"))

        except FileNotFoundError:
            self.table.setRowCount(0)
