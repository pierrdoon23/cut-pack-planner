from PyQt5.QtWidgets import ( QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QLineEdit, QComboBox, QSizePolicy, QCheckBox, QTableWidgetItem )
from .translations import tr
from ui.widgets import CommonWidgets

class PackagesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(CommonWidgets.build_header(tr('packages')))
        # Контент на всю ширину
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 10, 20, 10)
        content_layout.setSpacing(20)
        # ----- Форма добавления -----
        form_layout = QHBoxLayout()

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Введите ID рулона")
        self.id_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.id_input.setMaximumWidth(200)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Стандартный", "Вакуумный"])
        self.type_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.type_combo.setMaximumWidth(200)

        self.seam_combo = QComboBox()
        self.seam_combo.addItems(["Прямой", "Полукруглый (R50)"])
        self.seam_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.seam_combo.setMaximumWidth(200)

        self.width_input = QLineEdit("200")
        self.width_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.width_input.setMaximumWidth(200)
        self.length_input = QLineEdit("300")
        self.length_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.length_input.setMaximumWidth(200)
        self.count_input = QLineEdit("100")
        self.count_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.count_input.setMaximumWidth(200)

        self.double_cut = QCheckBox("Нарезка в два потока")
        self.tape_label = QCheckBox("Наклейка на ленту")

        self.add_button = QPushButton("Добавить задание")
        self.add_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.add_button.setMaximumWidth(200)
        form_layout.addStretch()

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

        content_layout.addLayout(form_layout)
        # ----- Таблица заданий -----
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID рулона", "Тип пакета", "Тип шва",
            "Размеры (мм)", "Количество", "Два потока",
            "На ленте", ""
        ])
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setMaximumWidth(1200)
        self.table.setMinimumWidth(600)
        content_layout.addWidget(QLabel("\nСписок заданий на нарезку пакетов"))
        content_layout.addWidget(self.table)
        content_layout.addStretch()
        layout.addLayout(content_layout)
        layout.addWidget(CommonWidgets.build_footer())
        self.setLayout(layout)
        self.setMaximumWidth(1200)
        self.setMinimumWidth(600)

        # Оставляем пустую таблицу, загрузка будет через API в будущем
        self.table.setRowCount(0)
