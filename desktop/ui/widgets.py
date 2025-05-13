from PyQt5.QtWidgets import ( QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame )
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from .translations import tr

class NavButton(QPushButton):
    def __init__(self, text, icon, callback, group):
        super().__init__(text)
        self.setIcon(icon)
        self.setCheckable(True)
        self.clicked.connect(lambda: self.activate(group, callback))
        self.setStyleSheet("padding: 10px; text-align: left;")

    def activate(self, group, callback):
        for btn in group:
            btn.setChecked(False)
        self.setChecked(True)
        callback()

class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(self.build_header())
        layout.addLayout(self.build_content())
        layout.addWidget(self.build_footer())

    def build_header(self):
        header = QFrame()
        header.setObjectName("Header")
        header.setLayout(QHBoxLayout())
        label = QLabel(tr('statistics'))
        label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        header.layout().addWidget(label)
        return header

    def build_footer(self):
        footer = QFrame()
        footer.setObjectName("Footer")
        footer.setLayout(QHBoxLayout())
        footer.layout().addWidget(QLabel("Footer content here"))
        return footer

    def build_content(self):
        vbox = QVBoxLayout()
        cards_layout = QHBoxLayout()
        self.add_stat_card(cards_layout, tr('rolls'), "48", "+4 за 24ч")
        self.add_stat_card(cards_layout, tr('cutting_maps'), "12", "+2 за 24ч")
        self.add_stat_card(cards_layout, tr('packages'), "36", "+8 за 24ч")
        vbox.addLayout(cards_layout)

        charts_layout = QHBoxLayout()
        charts_layout.addWidget(self.create_bar_chart())
        charts_layout.addWidget(self.create_donut_chart(tr('cutting_types'), [58, 42], ["Уголки", "Ленты"]))
        charts_layout.addWidget(self.create_donut_chart(tr('usage_and_waste'), [80, 20], ["Использовано", "Отходы"], ["green", "red"]))
        vbox.addLayout(charts_layout)
        return vbox

    def add_stat_card(self, layout, title, value, subtitle):
        card = QVBoxLayout()
        card.addWidget(QLabel(title))
        val = QLabel(value)
        val.setStyleSheet("font-size: 24px;")
        card.addWidget(val)
        sub = QLabel(subtitle)
        sub.setStyleSheet("color: gray;")
        card.addWidget(sub)
        w = QWidget()
        w.setLayout(card)
        w.setStyleSheet("background: #f5f5f5; border-radius: 10px; padding: 10px;")
        layout.addWidget(w)

    def create_bar_chart(self):
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.bar(["Пн", "Вт", "Ср", "Чт", "Пт"], [5, 7, 3, 8, 6], color='skyblue')
        return FigureCanvas(fig)

    def create_donut_chart(self, title, values, labels, colors=None):
        fig, ax = plt.subplots(figsize=(2.5, 2.5))
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90,
               colors=colors, wedgeprops=dict(width=0.4))
        ax.set_title(title)
        return FigureCanvas(fig)