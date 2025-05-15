from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QTableWidget, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import json
import os
from ui.translations import tr
from ui.widgets import CommonWidgets


class ReportPage(QWidget):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(CommonWidgets.build_header(tr('report')))
        self.header = QLabel(tr("report_text"))
        self.view_selector = QComboBox()
        self.view_selector.addItems(["📋 Таблица", "📈 Диаграмма Ганта"])
        self.view_selector.currentIndexChanged.connect(self.update_view)

        layout.addWidget(self.header)
        layout.addWidget(self.view_selector)

        self.view_area = QVBoxLayout()
        layout.addLayout(self.view_area)
        layout.addWidget(CommonWidgets.build_footer())

        self.load_data()
        self.update_view()

    def load_data(self):
        # Абсолютный путь к data3.json
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, "..", "data", "data3.json")
        json_path = os.path.abspath(json_path)

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
                print(f"✅ Загружено задач: {len(self.tasks)} из {json_path}")
        except FileNotFoundError:
            print(f"❌ Файл не найден по пути: {json_path}")
            self.tasks = []
        except json.JSONDecodeError as e:
            print(f"❌ Ошибка чтения JSON: {e}")
            self.tasks = []

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
        table = QTableWidget(len(self.tasks), 4)
        table.setHorizontalHeaderLabels(["ID", "Название", "Начало", "Конец"])
        for row, task in enumerate(self.tasks):
            table.setItem(row, 0, QTableWidgetItem(task.get("id", "")))
            table.setItem(row, 1, QTableWidgetItem(task.get("name", "")))
            table.setItem(row, 2, QTableWidgetItem(task.get("start", "")))
            table.setItem(row, 3, QTableWidgetItem(task.get("end", "")))
        self.view_area.addWidget(table)

    def show_gantt(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        colors = {"Запланировано": "skyblue", "В процессе": "orange", "Завершено": "green"}

        for i, task in enumerate(self.tasks):
            try:
                start = datetime.datetime.strptime(task["start"], "%Y-%m-%d")
                end = datetime.datetime.strptime(task["end"], "%Y-%m-%d")
                ax.barh(task["name"], (end - start).days, left=start, color=colors.get(task["status"], "gray"))
            except Exception as e:
                print(f"Ошибка при построении диаграммы задачи {task.get('id', '?')}: {e}")

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.set_xlabel("Дата")
        ax.set_ylabel("Задача")
        ax.grid(True)
        fig.autofmt_xdate()

        canvas = FigureCanvas(fig)
        self.view_area.addWidget(canvas)
