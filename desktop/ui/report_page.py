from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QTableWidget, QTableWidgetItem, QSizePolicy, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from ui.translations import tr
from ui.widgets import CommonWidgets


class ReportPage(QWidget):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.init_ui()
        self.setMaximumWidth(1200)
        self.setMinimumWidth(600)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(CommonWidgets.build_header(tr('report')))
        # Контент на всю ширину
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 10, 20, 10)
        content_layout.setSpacing(20)
        self.header = QLabel(tr("report_text"))
        self.header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.view_selector = QComboBox()
        self.view_selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.view_selector.addItems(["📋 Таблица", "📈 Диаграмма Ганта"])
        self.view_selector.currentIndexChanged.connect(self.update_view)

        content_layout.addWidget(self.header)
        content_layout.addWidget(self.view_selector)

        self.view_area = QVBoxLayout()
        content_layout.addLayout(self.view_area)
        content_layout.addStretch()
        layout.addLayout(content_layout)
        layout.addWidget(CommonWidgets.build_footer())

        self.update_view()

    def update_view(self):
        # Очистить старые виджеты
        while self.view_area.count():
            item = self.view_area.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        mode = self.view_selector.currentText()
        if "Таблица" in mode:
            self.show_table()
        else:
            self.show_gantt()

    def show_table(self):
        table = QTableWidget(0, 4)
        table.setHorizontalHeaderLabels(["ID", "Название", "Начало", "Конец"])
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.setMaximumWidth(1000)
        self.view_area.addWidget(table)

    def show_gantt(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.set_xlabel("Дата")
        ax.set_ylabel("Задача")
        ax.grid(True)
        fig.autofmt_xdate()
        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas.setMaximumWidth(1000)
        self.view_area.addWidget(canvas)
