from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import requests
from ui.translations import tr
from ui.widgets import CommonWidgets


class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(CommonWidgets.build_header(tr('statistics')))
        layout.addLayout(self.build_content())
        layout.addWidget(CommonWidgets.build_footer())

    def build_content(self):
        vbox = QVBoxLayout()

        # --- Загрузка всех данных с API ---
        stats = self.fetch_data("http://localhost:8000/stats")
        bar_data = self.fetch_data("http://localhost:8000/bar_chart")
        donut_cutting = self.fetch_data("http://localhost:8000/donut_cutting")
        donut_usage = self.fetch_data("http://localhost:8000/donut_usage")

        # --- Статистические карточки ---
        cards_layout = QHBoxLayout()
        for stat in stats:
            self.add_stat_card(cards_layout, tr(stat['name']), str(stat['value']), stat['change'])
        vbox.addLayout(cards_layout)

        # --- Графики ---
        charts_layout = QHBoxLayout()

        # Гистограмма
        bar_chart_layout = QVBoxLayout()
        title = QLabel(tr('plan_completion'))
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 5px;")
        bar_chart_layout.addWidget(title)
        bar_chart_layout.addWidget(self.create_bar_chart(bar_data))
        charts_layout.addLayout(bar_chart_layout)

        # Кольцевые диаграммы
        charts_layout.addWidget(self.create_donut_chart(tr('cutting_types'), donut_cutting))
        charts_layout.addWidget(self.create_donut_chart(tr('usage_and_waste'), donut_usage))

        vbox.addLayout(charts_layout)
        return vbox

    def fetch_data(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка загрузки с {url}: {response.status_code}")
                return []
        except Exception as e:
            print(f"Ошибка подключения к {url}:", e)
            return []

    def add_stat_card(self, layout, title, value, subtitle):
        card = QVBoxLayout()

        label_title = QLabel(title)
        label_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        card.addWidget(label_title)

        val = QLabel(value)
        val.setStyleSheet("font-size: 26px; font-weight: bold; color: #333333;")
        card.addWidget(val)

        sub = QLabel(subtitle)
        sub.setStyleSheet("color: gray; font-size: 12px;")
        card.addWidget(sub)

        w = QWidget()
        w.setLayout(card)
        w.setStyleSheet("background: #f5f5f5; border-radius: 10px; padding: 10px;")
        layout.addWidget(w)

    def create_bar_chart(self, data):
        labels = data.get("labels", [])
        values = data.get("values", [])
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.bar(labels, values, color='skyblue')
        ax.set_ylabel("Кол-во")
        fig.tight_layout()
        return FigureCanvas(fig)

    def create_donut_chart(self, title, data):
        values = data.get("values", [])
        labels = data.get("labels", [])
        colors = data.get("colors", None)

        fig, ax = plt.subplots(figsize=(2.5, 2.5))
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90,
               colors=colors, wedgeprops=dict(width=0.4))
        ax.set_title(title, fontsize=12)
        fig.tight_layout()
        return FigureCanvas(fig)
