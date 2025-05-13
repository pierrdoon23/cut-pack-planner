# ui/__init__.py

"""
UI package for the cutting optimizer app.
Contains page components, main window logic, and shared widgets.
"""
from .main_window import MainWindow
from .main_page import MainPage
from .visualization_page import VisualizationPage
from .packages_page import PackagesPage
from .settings_page import SettingsPage
from .widgets import CommonWidgets, NavButton
from .translations import tr