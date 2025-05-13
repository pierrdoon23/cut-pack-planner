# theme
light_theme = """
QWidget { background: #ffffff; color: #333333; }
QPushButton { background-color: #007BFF; color: white; border-radius: 5px; padding: 6px; }
QPushButton:checked { background-color: #6CA0DC; }
QLabel { color: #333333; }
QLineEdit { border: 1px solid #ccc; padding: 4px; border-radius: 3px; }
QComboBox { padding: 4px; }
QFrame#Header, QFrame#Footer, QFrame#Navbar { border: 1px solid black; }
"""

dark_theme = """
QWidget { background: #121212; color: #E0E0E0; }
QPushButton { background-color: #FFA726; color: black; border-radius: 5px; padding: 6px; }
QPushButton:checked { background-color: #424242; }
QLabel { color: #E0E0E0; }
QLineEdit { background: #1e1e1e; border: 1px solid #424242; color: white; padding: 4px; border-radius: 3px; }
QComboBox { background: #1e1e1e; color: white; padding: 4px; }
QFrame#Header, QFrame#Footer, QFrame#Navbar { border: 1px solid white; }
"""

current_theme = 'light'