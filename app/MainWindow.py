from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon
from .utils import assets_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowIcon(QIcon(assets_path.get('assets//app.ico')))
        self.setWindowTitle("Hello from HardCode!")
        self.setGeometry(100, 100, 800, 600)