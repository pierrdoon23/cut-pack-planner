from PyQt5.QtWidgets import ( QLabel, QPushButton, QHBoxLayout, QFrame )
from ui.translations import tr

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

class CommonWidgets():

    @staticmethod
    def build_header(title):
        header = QFrame()
        header.setObjectName("Header")
        header.setLayout(QHBoxLayout())
        header.setFixedHeight(60)
        header.layout().setContentsMargins(20, 0, 20, 0)
        header.layout().setSpacing(0)
        label = QLabel(title)
        label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px 0;")
        header.layout().addWidget(label)
        header.setStyleSheet("background: #fff; border-bottom: 1px solid #e0e0e0;")
        return header

    @staticmethod
    def build_footer():
        footer = QFrame()
        footer.setObjectName("Footer")
        footer.setFixedHeight(40)
        footer.setLayout(QHBoxLayout())
        footer.layout().setContentsMargins(20, 0, 20, 0)
        footer.layout().setSpacing(0)
        footer.layout().addWidget(QLabel("© 2025 Оптимизация раскроя. Все права защищены."))
        footer.setStyleSheet("background: #fff; border-top: 1px solid #e0e0e0;")
        return footer