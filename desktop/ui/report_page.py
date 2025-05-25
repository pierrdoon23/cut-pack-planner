from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QComboBox, QLabel, QTableWidget,
    QTableWidgetItem, QSizePolicy
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import requests

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

        self.fetch_tasks()
        self.update_view()

    def fetch_tasks(self):
        try:
            response = requests.get("http://localhost:8000/reports/tasks")
            response.raise_for_status()
            self.tasks = response.json()
        except Exception as e:
            print("Ошибка загрузки задач:", e)
            self.tasks = []

    def update_view(self):
        # Очистить старые виджеты
        while self.view_area.count():
            item = self.view_area.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        mode = self.view_selector.currentText()
        if "Таблица" in mode:
            self.show_table()
        else:
            self.show_gantt()

    def show_table(self):
        table = QTableWidget(len(self.tasks), 4)
        table.setHorizontalHeaderLabels(["ID", "Название", "Начало", "Конец"])

        for row, task in enumerate(self.tasks):
            table.setItem(row, 0, QTableWidgetItem(str(task["id"])))
            table.setItem(row, 1, QTableWidgetItem(task["name"]))
            table.setItem(row, 2, QTableWidgetItem(task["start_time"]))
            table.setItem(row, 3, QTableWidgetItem(task["end_time"] or "—"))

        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.setMaximumWidth(1000)
        self.view_area.addWidget(table)

    def show_gantt(self):
        fig, ax = plt.subplots(figsize=(8, 5))

        task_labels = []
        for i, task in enumerate(self.tasks):
            if not task["end_time"]:
                continue
            try:
                start = datetime.fromisoformat(task["start_time"])
                end = datetime.fromisoformat(task["end_time"])
                duration = (end - start).total_seconds() / 3600  # в часах

                ax.barh(i, duration, left=start, height=0.4)
                task_labels.append(task["name"])
            except Exception as e:
                print(f"Ошибка в задаче {task['id']}: {e}")

        ax.set_yticks(range(len(task_labels)))
        ax.set_yticklabels(task_labels)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))
        ax.set_xlabel("Дата / Время")
        ax.set_ylabel("Задача")
        ax.grid(True)

        fig.autofmt_xdate()

        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas.setMaximumWidth(1000)
        self.view_area.addWidget(canvas)
